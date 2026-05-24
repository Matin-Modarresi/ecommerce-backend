from django.contrib import admin
from django.contrib.admin.models import LogEntry
import os
from tempfile import NamedTemporaryFile
from django.http import StreamingHttpResponse
from django.utils.encoding import smart_str
from openpyxl import Workbook


class FileIterator:

    def __init__(self, file_path, chunk_size=8192):
        self.file_path = file_path
        self.chunk_size = chunk_size

    def __iter__(self):
        with open(self.file_path, "rb") as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                yield chunk


def export_logs_as_xlsx_streaming(model_admin, request, queryset):
    queryset = queryset.select_related("user", "content_type")

    tmp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
    tmp_path = tmp_file.name
    tmp_file.close()

    try:
        wb = Workbook(write_only=True)
        ws = wb.create_sheet(title="Audit Logs")

        headers = [
            "action_time",
            "user",
            "content_type",
            "object_id",
            "object_repr",
            "action_flag",
            "change_message",
        ]
        ws.append(headers)

        for log in queryset.iterator():
            ws.append([
                smart_str(log.action_time),
                smart_str(log.user),
                smart_str(log.content_type),
                smart_str(log.object_id),
                smart_str(log.get_action_flag_display()),
                smart_str(log.change_message),
            ])

        wb.save(tmp_path)
        wb.close()

        response = StreamingHttpResponse(
            FileIterator(tmp_path),
            content_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
        )

        def cleanup_file(response):
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        response._cleanup_file = cleanup_file

        return response

    except Exception:
        # در صورت خطا فایل را پاک کن
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("action_time", "user", "content_type", "object_repr", "action_flag", "change_message")
    list_filter = ("user", "content_type", "action_time")
    search_fields = ("object_repr", "change_message")
    readonly_fields = ("action_time", "user", "content_type", "object_id",
                       "object_repr", "action_flag", "change_message",)
    actions = [export_logs_as_xlsx_streaming]

    def has_add_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False


