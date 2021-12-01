from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "C:\\Users\\bikmu\\Desktop\\Thomas More\\Big Data\\Homework\\resources\\chromedriver.exe"

wd = webdriver.Chrome(PATH)


def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

	# open google image -> input what you want -> ctrl+c URL -> ctrl+v URL here:
    url = "https://www.google.com/search?rlz=1C1CHZN_enRU968RU968&sxsrf=AOaemvLk4klL6V1qdFoA_wFTUXm0kj-5uA:1638033113214&source=univ&tbm=isch&q=dogs+photo&fir=gM3Cz7MsHS_tAM%252CKsJYrmMqZTl1fM%252C_%253BbtQ8-aZ4x2YyMM%252CFofFudZ0yWjNIM%252C_%253BKua_EAQ5UETAiM%252CYFu-oWduMmqK_M%252C_%253Ba04b21q_maWyjM%252CKsJYrmMqZTl1fM%252C_%253Bs0Hfx2334Q3hfM%252C7ibyH0vDAkJUuM%252C_%253BaI2YUMxz3mLjzM%252CjIAijyd6DZqF7M%252C_%253Bcz7wF32Ml6xoCM%252COBh1eXSFpXCdlM%252C_%253BzN4s0B4hDUnyZM%252Cr8CEVxOSUXlofM%252C_%253BNJd0jRpJac0ynM%252Ce4H4tW6pxCMovM%252C_%253Bi8__JR5jsTLauM%252CVGirYKV8sLnrzM%252C_%253Ba713qY-ESW7b_M%252C044riAgE12UmZM%252C_%253BUTv9GTolHBCLFM%252CKsJYrmMqZTl1fM%252C_%253BSMMlmWDadP14fM%252C_RVRngRfeprTTM%252C_%253BbMD7fypnSVH1iM%252Cp8QQTw6sMvGK1M%252C_&usg=AI4_-kSjNSEM7wSc_BlxlVENlKJABm_DvQ&sa=X&ved=2ahUKEwiomN_uhLn0AhWE-KQKHdVZCxcQsAR6BAgCEAM&biw=1396&bih=691&dpr=1.38"

    # load the page
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        # get all image thumbnail results
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            
			# try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            # extract image urls
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)


# (wd, delay, max_images(change it if you want more))
urls = get_images_from_google(wd, 1, 300)

for i, url in enumerate(urls):
    # folder to save img
    download_image("dogs/", url, str(i) + ".jpg")

wd.quit()
