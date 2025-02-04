from django.apps import AppConfig

class SkincareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skincare'
    verbose_name = 'AI Skincare Companion'

    def ready(self):
        """
        Được gọi khi ứng dụng sẵn sàng
        Có thể thêm các tác vụ khởi tạo ở đây
        """
        pass 