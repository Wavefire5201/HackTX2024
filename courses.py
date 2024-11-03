import os
import sys
import re

import canvasapi
from canvasapi.course import Course
from canvasapi.module import Module, ModuleItem
from canvasapi.file import File
from canvasapi.page import Page
from canvasapi.exceptions import Unauthorized, ResourceDoesNotExist, Forbidden
from pathvalidate import sanitize_filename


class CourseDownloader:
    def __init__(self):
        self.DOWNLOAD_PATH = "./files"
        self.CANVAS_API_KEY = os.getenv("CANVAS_API_KEY")
        self.CANVAS_HOST = os.getenv("CANVAS_HOST")
        self.canvas = canvasapi.Canvas(
            "https://utexas.instructure.com", self.CANVAS_API_KEY
        )
        self.courses = self.canvas.get_courses()
        self.files_downloaded = set()

    def download_all(self):
        for course in self.courses:
            self.download_course(course)

    def download_course(self, course: Course):
        for module in course.get_modules():
            self.download_module(module)

    def download_module(self, module: Module):
        for item in module.get_module_items():
            self.download_item(item)

    def download_item(self, item: ModuleItem):
        print(f"{item.type} | {item}")
        path = f"{self.DOWNLOAD_PATH}/{item.course_id}/{item.module_id}/"
        # print(path)
        item1 = {key: value for key, value in item.__dict__.items()}
        # print(item1)
        if not os.path.exists(path):
            os.makedirs(path)

        course: Course = self.canvas.get_course(item.course_id)
        if item.type == "File":
            print(item)
            print(item.content_id)
            print(item.id)
            self.download_file(course, item.content_id, path)
        elif item.type == "Page":
            page: Page = course.get_page(item.page_url)
            with open(
                f"{path}{item.id}.html",
                "w",
                encoding="utf-8",
            ) as f:
                try:
                    f.write(page.body or "")
                except Exception as e:
                    print(e)
            files = self.extract_files(page.body or "")
            for file_id in files:
                self.download_file(course, file_id, path)

        elif item.type == "Assignment":
            assignment = course.get_assignment(item.content_id)
            with open(
                f"{path}{item.id}.html",
                "w",
                encoding="utf-8",
            ) as f:
                try:
                    f.write(assignment.description or "")
                except Exception as e:
                    print(e)
            files = self.extract_files(assignment.description or "")
            for file_id in files:
                self.download_file(course, file_id, path)

    def download_file(self, course: Course, content_id: int, path: str):
        if content_id in self.files_downloaded:
            return
        try:
            file: File = course.get_file(content_id)
            item1 = {key: value for key, value in file.__dict__.items()}
            print(item1)
            print(file.id, file.filename)
            print(file.filename.split())
            extension = file.filename.split(".")[-1] or ""
            dest_path = f"{path}{file.id}{"." + extension}"

            if os.path.isfile(dest_path):
                print("Skipping... File already exists...")
                pass

            self.files_downloaded.add(content_id)
            file.download(dest_path)

        except ResourceDoesNotExist or Unauthorized or Forbidden:
            pass

    def testing(self):
        temp = self.canvas.get_current_user().get_profile()
        print(temp)

        courses = self.canvas.get_courses()
        for course in courses:
            self.download_course(course, course.id)
            course: Course = course
            print("COURSE: ", course, course.id)
            for module in course.get_modules():
                print("MODULE: ", module, module.id)
                for item in module.get_module_items():
                    print("ITEM: ", item, item.type, item.id)
            # if item.type == "File":
            # self.download_item(item.id)
            # else:
            #     item1 = {key: value for key, value in item.__dict__.items()}
            #     print(item1)

            # if item.type == "File":
            #     self.download_item(item)

    def extract_files(self, text) -> set:
        text_search = re.findall("/files/(\\d+)", text, re.IGNORECASE)
        groups = set(text_search)
        return groups


def main():
    downloader = CourseDownloader()
    downloader.download_all()
    # downloader.testing()
    # downloader.downloader()


if __name__ == "__main__":
    main()
