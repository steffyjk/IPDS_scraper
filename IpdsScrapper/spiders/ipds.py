import scrapy
from scrapy.http import FormRequest
import requests

from IpdsScrapper.utils import convert_captcha_to_digits


class IpdsSpider(scrapy.Spider):
    name = "ipds"
    allowed_domains = ["ipds.gujarat.gov.in"]
    start_urls = ["https://ipds.gujarat.gov.in/Register/frm_RationCardAbstract.aspx"]

    def parse(self, response):
        # Assuming you've identified the image element using a CSS selector
        img_element = response.css('img')[0]
        if img_src := img_element.attrib.get('src'):
            # Download the image using requests
            img_response = requests.get(response.urljoin(img_src))
            if img_response.status_code == 200:
                with open("captcha_image.jpg", "wb") as f:
                    f.write(img_response.content)

            captcha = convert_captcha_to_digits()
            print("THIS IS CAPTCHA: ", captcha)
            try:
                formdata = {
                    'CaptchaControl1': str(captcha),
                    # Other form fields here
                }

                yield FormRequest.from_response(
                    response,
                    formdata=formdata,
                    callback=self.after_captcha_submit
                )
            except Exception as er:
                print("There is some err in captcha resolving", er)
        else:
            print("THERE IS SOMETHING WRONG")

    @staticmethod
    def after_captcha_submit(response):
        print("Captcha resolved successfully")
        # Capture a screenshot of the current page



    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)
