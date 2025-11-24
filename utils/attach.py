import allure
from allure_commons.types import AttachmentType


def add_screenshot(driver):
    """Добавить скриншот в Allure отчет"""
    png = driver.get_screenshot_as_png()
    allure.attach(
        body=png,
        name="Screenshot",
        attachment_type=AttachmentType.PNG,
        extension=".png"
    )


def add_logs(driver):
    """Добавить логи браузера в Allure отчет"""
    try:
        logs = driver.get_log("browser")
        log_str = "\n".join([f"{log['level']}: {log['message']}" for log in logs])
        allure.attach(
            body=log_str,
            name="Browser Logs",
            attachment_type=AttachmentType.TEXT,
            extension=".log"
        )
    except Exception as e:
        allure.attach(
            body=f"Could not get browser logs: {str(e)}",
            name="Browser Logs Error",
            attachment_type=AttachmentType.TEXT,
            extension=".log"
        )


def add_html(driver):
    """Добавить HTML страницы в Allure отчет"""
    html = driver.page_source
    allure.attach(
        body=html,
        name="Page Source",
        attachment_type=AttachmentType.HTML,
        extension=".html"
    )


def add_video(driver):
    """Добавить ссылку на видео в Allure отчет"""
    # Selenoid сохраняет видео по URL сессии
    video_url = f"https://selenoid.autotests.cloud/video/{driver.session_id}.mp4"
    html = f'<html><body><video width="100%" height="100%" controls autoplay>' \
           f'<source src="{video_url}" type="video/mp4"></video></body></html>'
    allure.attach(
        body=html,
        name="Video",
        attachment_type=AttachmentType.HTML,
        extension=".html"
    )