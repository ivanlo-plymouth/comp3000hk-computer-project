import os
import pandas as pd
import io
import asyncio
from arsenic import get_session, keys, browsers, services
from PIL import Image


async def create_html_file(subject, message, file_name):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container {{
                width: 50%;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>{subject}</h2>
            <p>{message}</p>
        </div>
    </body>
    </html>
    """

    def write_file():
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html_template)

    await asyncio.to_thread(write_file)


async def capture_screenshot(url, output_file, session):
    await session.get(url)

    total_height = int(await session.execute_script("return document.body.scrollHeight"))
    min_height = 1080
    viewport_height = max(total_height, min_height)

    await session.set_window_size(1920, viewport_height)

    screenshot = await session.get_screenshot()

    # Convert the PNG image to a JPG image
    png_image = Image.open(io.BytesIO(screenshot.getvalue()))
    jpg_image = png_image.convert("RGB")

    def write_file():
        with open(output_file, "wb") as f:
            jpg_image.save(f, "JPEG", quality=90)  # You can adjust the quality parameter (0-100)

    await asyncio.to_thread(write_file)

## PNG format
# async def capture_screenshot(url, output_file, session):
#     await session.get(url)

#     # Set viewport height to the total height of the page
#     total_height = int(await session.execute_script("return document.body.scrollHeight"))

#     # Set a minimum height for the viewport
#     min_height = 1080  # You can change this value according to your needs

#     # Use the maximum of total height and minimum height
#     viewport_height = max(total_height, min_height)

#     await session.set_window_size(1920, viewport_height)

#     screenshot = await session.get_screenshot()

#     def write_file():
#         with open(output_file, "wb") as f:
#             f.write(screenshot.getvalue())

#     await asyncio.to_thread(write_file)


async def process_row(index, row, session):
    html_file_name = f"html_files/{index}.html"
    screenshot_file_name = f"screenshots/{index}.png"

    await create_html_file(row["subject"], row["message"], html_file_name)
    await capture_screenshot(f"file:///{os.path.abspath(html_file_name)}", screenshot_file_name, session)


async def main():
    data = pd.read_csv("csv/Book1.csv")

    os.makedirs("html_files", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)

    labeled_screenshots = pd.DataFrame(columns=["filename", "label"])

    service = services.Chromedriver(binary='./chromedriver')
    browser = browsers.Chrome(
        **{"goog:chromeOptions": {"args": ["--headless", "--disable-gpu"]}}
    )

    async with get_session(service, browser) as session:
        for index, row in data.iterrows():
            html_file_name = f"html_files/{index}.html"
            screenshot_file_name = f"screenshots/{index}.jpeg"

            await create_html_file(row["subject"], row["message"], html_file_name)
            await capture_screenshot(f"file:///{os.path.abspath(html_file_name)}", screenshot_file_name, session)

            new_row = pd.DataFrame({"filename": [screenshot_file_name], "label": [row["label"]]})
            labeled_screenshots = pd.concat([labeled_screenshots, new_row], ignore_index=True)

    labeled_screenshots.to_csv("labeled_screenshots.csv", index=False)
    print("HTML files, screenshots, and labeled_screenshots.csv created.")


if __name__ == "__main__":
    asyncio.run(main())
