import requests
from flet import *
import time

from math import pi
# from response import responding
from threading import Timer, Thread


_BASE = "https://dubemguy.pythonanywhere.com"


# history_1 = {"hi": "hi, what do you want me to do", "hey": "hi, what do you want me to do"}
# model.start_chat(history=history_1)


def main(screen: Page):
    screen.title = "~Chat App"
    screen.window.always_on_top = True
    screen.window.width = 434.4
    screen.window.height = 682.4
    screen.theme_mode = ThemeMode.DARK
    screen.window.resizable = False
    screen.fonts = {"sf": "assets/sf-pro-display-font/SF-Pro-Display-Black.ttf",
                    "sf_text": "assets/sf-pro-display-font/SF-Pro-Display-Regular.otf",
                    "sf_light": "assets/sf-pro-display-font/SF-Pro-Display-Light.otf",
                    "sf_text_light": "assets/sf-pro-display-font/SF-Pro-Text-Light.otf",
                    "jetbrains_reg": "assets/ttf/JetBrainsMono-Regular.ttf",
                    "jetbrains_semi_bold": "assets/ttf/JetBrainsMono-SemiBold.ttf",
                    "jetbrains_light": "assets/ttf/JetBrainsMono-Light.ttf",
                    }

    def add_user_history():
        chats_history.content.controls[Var.inc_response].controls[2].offset = (0, 25)
        chats_history.content.controls[Var.inc_response].controls[0].offset = (-9, 0)
        chats_history.content.controls[Var.inc_response].controls[1].offset = (0, 23)
        chats_history.content.controls[Var.inc_response].update()
        Var.inc_response += 1

    def always_zero(pos: int):
        # print(chats_history.content.controls[Var.inc_response].controls[2].offset)
        if chats_history.content.controls[Var.inc_response].controls[2].offset != (0, 0):
            chats_history.content.controls[Var.inc_response].controls[2].offset = (0, 0)
            chats_history.content.controls[Var.inc_response].controls[0].offset = (0, 0)
            chats_history.content.controls[Var.inc_response].controls[1].offset = (0, 0)
            chats_history.content.controls[Var.inc_response].update()
        Var.inc_response += 1

    def add_ai_history():
        chats_history.content.controls[Var.inc_response].controls[2].offset = (0, 25)
        chats_history.content.controls[Var.inc_response].controls[0].offset = (-9, 0)
        chats_history.content.controls[Var.inc_response].controls[1].offset = (0, 23)
        chats_history.content.controls[Var.inc_response].update()
        Timer(0.5, always_zero, kwargs={"pos": Var.inc_response}).start()

    def blur_background():
        if not Var.blur_condition:
            Var.blur_condition = True
            for blur_inc in range(0, 301):
                Background_check.controls[0].blur = blur_inc / 100
                time.sleep(0.1)
                Background_check.update()

    class Var:
        inc_response: int = 1
        blur_condition: bool = False
        start: int = 0

        def send_message(self, message, package):
            condition = True
            while condition:
                try:
                    if requests.get("https://www.google.com").status_code == 200:
                        requests.put(_BASE + "/sensor/api", json={"user": message}, timeout=3)
                        # icons.DONE_ALL
                        package.controls[2].content.controls[1].name = icons.DONE_ALL
                        package.controls[2].content.controls[1].color = "green"
                        package.controls[2].content.controls[1].update()
                        break
                    else:
                        time.sleep(0.05)
                except:
                    pass

    def submit_response(e: ControlEvent):
        if not enter_text.controls[0].value == "":
            sent_text = user_respond(e.control.value)
            chats_history.content.controls.insert(-1, sent_text)
            e.control.scale = 1.0023233
            Timer(.01, Var().send_message, kwargs={"message": e.control.value, "package": sent_text}).start()
            e.control.value = ""

            e.control.update()
            chats_history.content.update()
            Timer(.6, add_user_history).start()
            Thread(blur_background()).start()
            # print(chats_history.content.controls, "hello world")

    def submit_play(e: ControlEvent):
        if not enter_text.controls[0].value == "":
            sent_text = user_respond(enter_text.controls[0].value)
            chats_history.content.controls.insert(-1, sent_text)
            # chats_history.content.controls.append(ai_respond(enter_text.controls[0].value))
            chats_history.content.update()
            e.control.content.rotate = 2 * pi
            e.control.content.scale = 0.45
            e.control.content.offset = (5, 0)
            Timer(1, Var().send_message, kwargs={"message": enter_text.controls[0].value, "package": sent_text}).start()
            enter_text.controls[0].value = ""

            chats_history.update()
            enter_text.update()
            e.control.update()

            Timer(.1, add_user_history).start()
            Thread(blur_background()).start()

        # print(e.control.data[0])

    def submit_play_end(e):
        e.control.offset = (0, 0)
        e.control.rotate = 0
        e.control.scale = 1
        e.control.update()

    def time_user_response(e):
        e.control.offset = (0, 0)
        e.control.update()

    def copy_die(e):
        main_page.controls.pop()
        screen.update()

    def copy(e: ContainerTapEvent):
        screen.set_clipboard(e.control.content.value)
        main_page.controls.append(
            Stack(alignment=alignment.center,
                  controls=[Container(width=screen.window.width, height=screen.window.height,
                                      alignment=alignment.center, bgcolor="",
                                      blur=10,
                                      padding=padding.only(top=5),
                                      content=Text(text_align=TextAlign.CENTER, style=TextStyle(
                                          font_family="Comic Sans MS",
                                          foreground=Paint(
                                              gradient=PaintRadialGradient(
                                                  (screen.window.width / 2,
                                                   screen.window.height / 2 - 60),
                                                  40,
                                                  [colors.PURPLE, colors.BLUE]
                                              ), style=PaintingStyle.FILL,
                                          ),
                                          letter_spacing=0.5), size=50, weight=FontWeight.W_600,
                                                   value="""Text Copied !!!""", opacity=0.75), on_click=copy_die),
                            ])
        )
        screen.update()

    def out_respond(text_said):
        if True:
            out_response = Column(horizontal_alignment=CrossAxisAlignment.START, width=screen.window.width - 4,
                                  spacing=2,
                                  controls=[
                                      Text(text_align=TextAlign.START, value="Dubem (🤪)", style=TextStyle(
                                          font_family="jetbrains_reg",
                                          letter_spacing=0.5), size=12, weight=FontWeight.W_600, offset=(-10, 0),
                                           animate_offset=animation.Animation(600, animation.AnimationCurve.DECELERATE),
                                           on_animation_end=time_user_response),
                                      Container(bgcolor=colors.GREY_800,
                                                border_radius=border_radius.only(0, 15, 15, 15),
                                                padding=padding.symmetric(horizontal=10, vertical=6),
                                                content=Text(text_align=TextAlign.END, style=TextStyle(
                                                    font_family="jetbrains_reg",
                                                    letter_spacing=0.5), size=17, weight=FontWeight.W_500,
                                                             color=colors.GREY_400,
                                                             value=text_said), offset=(0, 25),
                                                animate_offset=animation.Animation(900,
                                                                                   animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                                on_animation_end=time_user_response),

                                      Container(bgcolor=colors.TRANSPARENT,
                                                border_radius=border_radius.only(15, 15, 15, 15),
                                                padding=padding.symmetric(horizontal=5, vertical=0),
                                                content=Row(
                                                    alignment=MainAxisAlignment.START, spacing=5,
                                                    controls=[Text(text_align=TextAlign.START, style=TextStyle(
                                                        font_family="jetbrains_reg",
                                                        letter_spacing=0.5), size=12, weight=FontWeight.W_600,
                                                                   value=time.strftime("%I:%M %p")),
                                                              ]), offset=(0, 28),
                                                animate_offset=animation.Animation(900,
                                                                                   animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                                on_animation_end=time_user_response)
                                  ])

        return out_response

    def user_respond(wish):
        user_response = Column(horizontal_alignment=CrossAxisAlignment.END, width=screen.window.width - 4,
                               spacing=2,
                               controls=[
                                   Text(text_align=TextAlign.START, value="🔥My Babe", style=TextStyle(
                                       font_family="jetbrains_reg",
                                       letter_spacing=0.5), size=12, weight=FontWeight.W_600, offset=(-10, 0),
                                        animate_offset=animation.Animation(600, animation.AnimationCurve.DECELERATE),
                                        on_animation_end=time_user_response),
                                   Container(bgcolor=colors.GREY_800, border_radius=border_radius.only(15, 0, 15, 15),
                                             padding=padding.symmetric(horizontal=10, vertical=6),
                                             content=Text(text_align=TextAlign.END, style=TextStyle(
                                                 font_family="jetbrains_reg",
                                                 letter_spacing=0.5), size=17, weight=FontWeight.W_500,
                                                          color=colors.GREY_400,
                                                          value=wish), offset=(0, 25),
                                             animate_offset=animation.Animation(900,
                                                                                animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                             on_animation_end=time_user_response),

                                   Container(bgcolor=colors.TRANSPARENT,
                                             border_radius=border_radius.only(15, 15, 15, 15),
                                             padding=padding.symmetric(horizontal=5, vertical=2),
                                             content=Row(
                                                 alignment=MainAxisAlignment.END, spacing=5,
                                                 controls=[Text(text_align=TextAlign.END, style=TextStyle(
                                                     font_family="jetbrains_reg",
                                                     letter_spacing=0.5), size=12, weight=FontWeight.W_600,
                                                                value=time.strftime("%I:%M %p")),
                                                           Icon(name=icons.ACCESS_TIME_ROUNDED, color="white", size=13),
                                                           ]), offset=(0, 28),
                                             animate_offset=animation.Animation(900,
                                                                                animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                             on_animation_end=time_user_response)
                               ])
        return user_response

    chats_history = Container(width=screen.window.width - 0, height=screen.window.height - 50, bgcolor="",
                              padding=padding.symmetric(horizontal=0),
                              border_radius=10,
                              # border=Border(left=BorderSide(width=3, color=colors.GREY_600),
                              #               right=BorderSide(width=3, color=colors.GREY_600),
                              #               top=BorderSide(width=3, color=colors.GREY_600),
                              #               bottom=BorderSide(width=3, color=colors.GREY_600)),
                              content=Column(width=screen.window.width - 6, height=screen.window.height - 50,
                                             alignment=MainAxisAlignment.START, auto_scroll=True, spacing=20,
                                             run_spacing=20,
                                             scroll=ScrollMode.AUTO,
                                             controls=[
                                                 Row(
                                                     alignment=MainAxisAlignment.CENTER,
                                                     controls=[
                                                         Container(
                                                             bgcolor=colors.BLACK26, border_radius=8,
                                                             alignment=alignment.top_center,
                                                             padding=padding.symmetric(2, 10),
                                                             content=Text(text_align=TextAlign.END, style=TextStyle(
                                                                 font_family="jetbrains_semi_bold",
                                                                 letter_spacing=0.5), size=17, weight=FontWeight.W_600,
                                                                          color=colors.GREY_600,
                                                                          value="Today")),
                                                     ],
                                                 ),

                                                 TransparentPointer(height=50),
                                                 # ai_respond("bro i am a bot, shut the f*ck up."),
                                                 # ai_respond(
                                                 #     "LangChain is a framework designed to simplify the creation of applications using large language models. As a language model integration framework, LangChain's use-cases largely overlap with those of language models in general, including document analysis and summarization, chatbots, and code analysis"),
                                             ]))

    enter_text = Row(alignment=MainAxisAlignment.SPACE_BETWEEN, bottom=1, right=0.5, left=0.5,
                     controls=[
                         CupertinoTextField(placeholder_text="Send A Message...", width=screen.window.width - 92,
                                            border_radius=8,
                                            expand=False,
                                            height=50,
                                            placeholder_style=TextStyle(color=colors.GREY_500,
                                                                        ),
                                            # border=border.all(3, colors.GREY_600),
                                            text_align=TextAlign.CENTER,
                                            text_style=TextStyle(
                                                font_family="jetbrains_reg",
                                                letter_spacing=1),
                                            multiline=True,
                                            max_lines=10,
                                            bgcolor=colors.GREY_900,
                                            text_size=17,
                                            cursor_color=colors.with_opacity(0.5, colors.GREY_500),
                                            cursor_height=26,
                                            autofocus=True,
                                            autocorrect=True,
                                            animate_scale=animation.Animation(500, animation.AnimationCurve.LINEAR),
                                            on_submit=submit_response,
                                            shift_enter=True,
                                            dense=True),
                         Container(content=IconButton(height=49, width=49,
                                                      content=Icon(name=cupertino_icons.PAPERPLANE, size=25,
                                                                   color=colors.GREY_600,
                                                                   scale=1, rotate=0, offset=(0, 0),
                                                                   animate_scale=animation.Animation(1200,
                                                                                                     animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                                                   animate_rotation=animation.Animation(1200,
                                                                                                        animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                                                   animate_offset=animation.Animation(1200,
                                                                                                      animation.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
                                                                   on_animation_end=submit_play_end,
                                                                   ),
                                                      on_click=submit_play,
                                                      data=[0],
                                                      style=ButtonStyle(shape={"": RoundedRectangleBorder(radius=6)},
                                                                        bgcolor=colors.GREY_900, color=colors.WHITE,
                                                                        overlay_color={
                                                                            MaterialState.PRESSED: colors.BLACK38})),
                                   height=50, width=50,
                                   alignment=alignment.center, border=border.all(1, colors.GREY_800),
                                   border_radius=border_radius.all(10))])

    def resize(e: ControlEvent):
        chats_history.width = screen.window.width - 0
        chats_history.height = screen.window.height - 50
        chats_history.content.width = screen.window.width - 6
        # user_response.width = screen.window.width - 4
        chats_history.content.height = screen.window.height - 120
        enter_text.width = screen.window.width - 0
        enter_text.controls[0].width = screen.window.width - 92
        main_page.controls[1].width = screen.window.width
        main_page.controls[1].height = screen.window.height - 55
        Background_check.controls[0].width = screen.window.width
        Background_check.controls[0].height = screen.window.height - 60
        main_page.width = screen.window.width
        main_page.height = screen.window.height - 50

        main_page.update()
        Background_check.update()
        enter_text.controls[0].update()
        chats_history.update()
        enter_text.update()
        # screen.window.height

    Background_check = Stack(alignment=alignment.center,
                             controls=[Container(width=screen.window.width, height=screen.window.height - 60,
                                                 alignment=alignment.center, bgcolor="",
                                                 padding=padding.only(top=5),
                                                 content=Image(src="""
                                                 data:image/svg+xml;base64, <?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
<svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="12" cy="12" r="3" stroke="#1C274C" stroke-width="1.5"/>
<path d="M13.7654 2.15224C13.3978 2 12.9319 2 12 2C11.0681 2 10.6022 2 10.2346 2.15224C9.74457 2.35523 9.35522 2.74458 9.15223 3.23463C9.05957 3.45834 9.0233 3.7185 9.00911 4.09799C8.98826 4.65568 8.70226 5.17189 8.21894 5.45093C7.73564 5.72996 7.14559 5.71954 6.65219 5.45876C6.31645 5.2813 6.07301 5.18262 5.83294 5.15102C5.30704 5.08178 4.77518 5.22429 4.35436 5.5472C4.03874 5.78938 3.80577 6.1929 3.33983 6.99993C2.87389 7.80697 2.64092 8.21048 2.58899 8.60491C2.51976 9.1308 2.66227 9.66266 2.98518 10.0835C3.13256 10.2756 3.3397 10.437 3.66119 10.639C4.1338 10.936 4.43789 11.4419 4.43786 12C4.43783 12.5581 4.13375 13.0639 3.66118 13.3608C3.33965 13.5629 3.13248 13.7244 2.98508 13.9165C2.66217 14.3373 2.51966 14.8691 2.5889 15.395C2.64082 15.7894 2.87379 16.193 3.33973 17C3.80568 17.807 4.03865 18.2106 4.35426 18.4527C4.77508 18.7756 5.30694 18.9181 5.83284 18.8489C6.07289 18.8173 6.31632 18.7186 6.65204 18.5412C7.14547 18.2804 7.73556 18.27 8.2189 18.549C8.70224 18.8281 8.98826 19.3443 9.00911 19.9021C9.02331 20.2815 9.05957 20.5417 9.15223 20.7654C9.35522 21.2554 9.74457 21.6448 10.2346 21.8478C10.6022 22 11.0681 22 12 22C12.9319 22 13.3978 22 13.7654 21.8478C14.2554 21.6448 14.6448 21.2554 14.8477 20.7654C14.9404 20.5417 14.9767 20.2815 14.9909 19.902C15.0117 19.3443 15.2977 18.8281 15.781 18.549C16.2643 18.2699 16.8544 18.2804 17.3479 18.5412C17.6836 18.7186 17.927 18.8172 18.167 18.8488C18.6929 18.9181 19.2248 18.7756 19.6456 18.4527C19.9612 18.2105 20.1942 17.807 20.6601 16.9999C21.1261 16.1929 21.3591 15.7894 21.411 15.395C21.4802 14.8691 21.3377 14.3372 21.0148 13.9164C20.8674 13.7243 20.6602 13.5628 20.3387 13.3608C19.8662 13.0639 19.5621 12.558 19.5621 11.9999C19.5621 11.4418 19.8662 10.9361 20.3387 10.6392C20.6603 10.4371 20.8675 10.2757 21.0149 10.0835C21.3378 9.66273 21.4803 9.13087 21.4111 8.60497C21.3592 8.21055 21.1262 7.80703 20.6602 7C20.1943 6.19297 19.9613 5.78945 19.6457 5.54727C19.2249 5.22436 18.693 5.08185 18.1671 5.15109C17.9271 5.18269 17.6837 5.28136 17.3479 5.4588C16.8545 5.71959 16.2644 5.73002 15.7811 5.45096C15.2977 5.17191 15.0117 4.65566 14.9909 4.09794C14.9767 3.71848 14.9404 3.45833 14.8477 3.23463C14.6448 2.74458 14.2554 2.35523 13.7654 2.15224Z" stroke="#1C274C" stroke-width="1.5"/>
</svg>
                                                 """, color=colors.BLACK,
                                                               width=screen.window.width,
                                                               height=screen.window.height - 60)),
                                       ])
    screen.on_resized = resize
    screen.vertical_alignment = MainAxisAlignment.CENTER
    screen.horizontal_alignment = CrossAxisAlignment.CENTER
    main_page = Stack(controls=[
        Background_check,
        Column(width=screen.window.width, height=screen.window.height, alignment=MainAxisAlignment.START,
               horizontal_alignment=CrossAxisAlignment.CENTER,
               spacing=0, run_spacing=0,
               controls=[chats_history]),
        enter_text,
    ], width=screen.window.width, height=screen.window.height - 50)
    screen.add(main_page)
    __reply = ""

    while True:
        try:
            if requests.get("https://www.google.com").status_code == 200:
                if requests.get(_BASE + "/sensor/api", timeout=1).json().get("dubs") == __reply:
                    continue
                else:
                    if requests.get(_BASE + "/sensor/api", timeout=1).json().get("dubs") != "":
                        chats_history.content.controls.insert(-1,
                                                              out_respond(requests.get(_BASE + "/sensor/api",
                                                                                       timeout=1).json().get("dubs"))
                                                              )
                        chats_history.update()
                        Thread(target=add_ai_history).run()
                    # icons.DONE_ALL
                    __reply = requests.get(_BASE + "/sensor/api", timeout=1).json().get("dubs")
            else:
                pass
        except:
            pass

    screen.update()


app(target=main, assets_dir='assets')
