import flet as ft
from kivy.core.audio import SoundLoader
from threading import Thread
import os
import time

# قائمة لتخزين الإحداثيات
speed_bumps = []

def main(page: ft.Page):
    page.window_icon = "C:\\Users\\awsat\\Desktop\\GPS\\assets\\icon.ico"
    page.title = "تطبيق GPS مع تنبيه المطبات"
    page.window_full_screen = True
    page.padding = 0
    page.bgcolor = ft.colors.BLACK

    # مسار الخلفية ومسار النغمة
    background_path = "C:/Users/awsat/Desktop/GPS/assets/background.png"
    tone_path = r"C:\Users\awsat\Desktop\GPS\assets\tone.mp3"  # تأكد من أن المسار صحيح وأن الملف موجود

    # مسافة التنبيه الافتراضية والمدة
    default_alert_distance = 90  # متر
    alert_duration = 8  # ثواني

    # دالة التنبيه عند الاقتراب من مطب
    def alert_near_speed_bump(bump_number, alert_distance):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"تنبيه: الاقتراب من مطب {bump_number} خلال {alert_distance} متر!", color=ft.colors.GREEN),
            bgcolor=ft.colors.RED,
            duration=alert_duration * 1000
        )
        page.snack_bar.open = True
        page.update()

    # دالة الفحص المستمر للمطبات
    def scan_for_speed_bumps(speed):
        # ضبط مسافة التنبيه بناءً على السرعة
        if speed < 80:
            alert_distance = 60
        elif 80 <= speed <= 90:
            alert_distance = 90
        else:
            alert_distance = 120

        while True:
            for i, bump in enumerate(speed_bumps, start=1):
                alert_near_speed_bump(i, alert_distance)
                play_tone()
                time.sleep(alert_duration)  # الانتظار لمدة التنبيه قبل التحقق من المطب التالي

    # دالة تشغيل النغمة
    def play_tone():
        print("جاري محاولة تشغيل النغمة...")
        if os.path.exists(tone_path):
            print(f"تم العثور على ملف النغمة في: {tone_path}")
            sound = SoundLoader.load(tone_path)
            if sound:
                sound.play()
                print("تم تشغيل النغمة بنجاح.")
            else:
                print("حدث خطأ في تحميل ملف النغمة.")
        else:
            print("لم يتم العثور على ملف النغمة. تأكد من صحة المسار.")

    # دالة الحفظ
    def save_location(e):
        coordinates = (31.678, 20.763)  # استبدلها بإحداثيات الموقع الحالي
        speed_bumps.append(coordinates)
        page.snack_bar = ft.SnackBar(
            content=ft.Text("تم حفظ الموقع بنجاح!", color=ft.colors.WHITE),
            bgcolor=ft.colors.GREEN,
            duration=2000
        )
        page.snack_bar.open = True
        page.update()

    # دالة عرض السجلات
    def show_records(e):
        records_content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(f"مطب {i+1}: {coord}", color=ft.colors.BLUE),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=i: delete_record(idx)),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
                for i, coord in enumerate(speed_bumps)
            ],
            spacing=10
        )
        
        page.dialog = ft.AlertDialog(
            title=ft.Text("سجلات المطبات", color=ft.colors.WHITE),
            content=records_content,
            actions=[ft.TextButton("إغلاق", on_click=lambda e: page.dialog.close())]
        )
        page.dialog.open = True
        page.update()

    # دالة الحذف
    def delete_record(index):
        del speed_bumps[index]
        show_records(None)

    # صفحة الإعدادات
    def settings_page(e):
        page.clean()
        settings_content = ft.Column(
            [
                ft.Slider(min=0, max=100, label="مستوى الصوت"),
                ft.ElevatedButton(
                    content=ft.Text("اختبار النغمة", size=18),
                    on_click=play_tone,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.BLUE,
                    width=250,
                    height=60,
                ),
                ft.ElevatedButton(
                    content=ft.Text("عرض السجلات", size=18),
                    on_click=show_records,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREY,
                    width=250,
                    height=60,
                ),
                ft.ElevatedButton(
                    content=ft.Text("العودة للصفحة الرئيسية", size=18),
                    on_click=main_page,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREY,
                    width=250,
                    height=60,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )
        page.add(settings_content)
        page.update()

    # عرض الصفحة الرئيسية
    def main_page(e=None):
        page.clean()
        background_image = ft.Image(
            src=background_path,
            fit=ft.ImageFit.COVER,
        )

        button_style = ft.ButtonStyle(
            padding=ft.padding.all(15),
            shape=ft.RoundedRectangleBorder(radius=8),
            shadow_color=ft.colors.BLACK,
            elevation=5,
        )

        # عرض المطبات المحفوظة في الصفحة الرئيسية مع الرقم التسلسلي
        bumps_display = ft.Column(
            [
                ft.Text(f"مطب {i+1}: إحداثيات {coord}", color=ft.colors.WHITE, size=18)
                for i, coord in enumerate(speed_bumps)
            ],
            spacing=10
        )

        content = ft.Column(
            [
                ft.Text("تطبيق GPS", size=30, color=ft.colors.WHITE, weight="bold"),
                bumps_display,  # عرض المطبات المحفوظة مع الرقم التسلسلي
                ft.ElevatedButton(
                    content=ft.Text("تشغيل التنبيه", size=18),
                    on_click=lambda e: Thread(target=scan_for_speed_bumps, args=(85,)).start(),  # سرعة افتراضية 85 كم/ساعة للتجربة
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.BLUE,
                    style=button_style,
                    width=250,
                    height=60,
                ),
                ft.ElevatedButton(
                    content=ft.Text("حفظ الموقع", size=18),
                    on_click=save_location,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREEN,
                    style=button_style,
                    width=250,
                    height=60,
                ),
                ft.ElevatedButton(
                    content=ft.Text("الإعدادات", size=18),
                    on_click=settings_page,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.YELLOW,
                    style=button_style,
                    width=250,
                    height=60,
                ),
                ft.ElevatedButton(
                    content=ft.Text("إغلاق التطبيق", size=18),
                    on_click=lambda e: page.window_close(),
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREY,
                    style=button_style,
                    width=250,
                    height=60,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )

        page.add(
            ft.Stack(
                [
                    background_image,
                    ft.Container(
                        content,
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(20),
                    ),
                ]
            )
        )
        page.update()

    main_page()

ft.app(target=main)
