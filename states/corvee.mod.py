from PIL import Image, ImageDraw, ImageFont
from time import sleep
from states.base import BaseState
from random import randint
import requests


class State(BaseState):
    # module information
    name = "corvee"
    index = 80
    delay = 3600

    # get corvee dashboard data
    @staticmethod
    def get_names():
        try:
            response = requests.get("https://corvee.djoamersfoort.nl/api/v1/selected")
        except requests.exceptions.RequestException:
            return []
        if not response.ok:
            return []
        return response.json()["selected"]

    # module check function
    def check(self, _state):
        return len(self.get_names()) > 0

    # runner function
    def run(self):
        elapsed = 0
        flash = False
        colors = [(randint(128, 255), randint(128, 255), randint(128, 255)),
                  (randint(128, 255), randint(128, 255), randint(128, 255)),
                  (randint(128, 255), randint(128, 255), randint(128, 255))]
        names = self.get_names()
        font_path = "/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf"

        while not self.killed:
            flash = not flash
            if elapsed < 3:
                image = Image.new("RGB", (96, 32),
                                  (randint(0, 255), randint(0, 255), randint(0, 255)) if flash else "black")
            else:
                image = Image.new("RGB", (96, 32), "black")

            draw = ImageDraw.Draw(image)

            if elapsed >= 14:
                font = ImageFont.truetype(font_path, size=11)
                for i in range(0, len(names)):
                    draw.text((48, 5 + 11 * i), names[i], fill=colors[i], anchor="mm", font=font)
                for i in range(0, 6):
                    y = (elapsed + i * 8) % 40
                    draw.rectangle([(2, y - 8), (8, y - 4)], fill="blue")
                    draw.rectangle([(88, y - 8), (94, y - 4)], fill="blue")

            elif elapsed >= 13:
                font = ImageFont.truetype(font_path, size=28)
                draw.text((72, 16), "1", fill="red", anchor="mm", font=font)
            elif elapsed >= 12:
                font = ImageFont.truetype(font_path, size=28)
                draw.text((48, 16), "2", fill="yellow", anchor="mm", font=font)
            elif elapsed >= 11:
                font = ImageFont.truetype(font_path, size=28)
                draw.text((24, 16), "3", fill="green", anchor="mm", font=font)
            elif elapsed >= 9:
                font = ImageFont.truetype(font_path, size=10)
                draw.text((48, 16), "...van vandaag\nzijn...", fill="yellow", anchor="mm", font=font)
            elif elapsed >= 7:
                font = ImageFont.truetype(font_path, size=10)
                draw.text((48, 16), "...voor het\ncorvee...", fill="yellow", anchor="mm", font=font)
            elif elapsed >= 5:
                font = ImageFont.truetype(font_path, size=10)
                draw.text((48, 16), "De grote\nwinnaars...", fill="yellow", anchor="mm", font=font)
            elif elapsed >= 3:
                font = ImageFont.truetype(font_path, size=24)
                draw.text((48, 16), "Hallo!", fill="cyan", anchor="mm", font=font)
            self.output_image(image)
            sleep(.1)
            elapsed += .1
