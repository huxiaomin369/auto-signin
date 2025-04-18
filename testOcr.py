import ddddocr
from seleniumwire import webdriver
import json

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from imageUtil import url_to_imageBytes,get_image_width

userName = "xxxx"
password = "xxxx"

debugMode = False


if __name__ == "__main__":
  myUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
  options = Options()
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-extensions')
  options.add_argument("disable-blink-features=AutomationControlled")
  options.add_argument(f'user-agent={myUserAgent}')
  options.add_experimental_option('excludeSwitches', ['enable-automation'])
  options.add_experimental_option('useAutomationExtension', False)
  if not debugMode:
    # 设置无头模式
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # 设置禁止加载图片的选项
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        'permissions.default.stylesheet': 2  # 同时禁止CSS加载
    }
    options.add_experimental_option("prefs", prefs)
  driver = None
  try:
      driver = webdriver.Chrome(options=options)
      driver.get("https://link-ai.tech/console/account")
      wait = WebDriverWait(driver, 5)
      tab_element = wait.until(
        EC.element_to_be_clickable((By.ID, "tab-second"))
      )
      tab_element.click()
      userNameInput = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".el-input__inner[placeholder='请输入手机号']"))
      )
      passWInput = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".el-input__inner[placeholder='请输入密码']"))
      )
      userNameInput.clear()  
      userNameInput.send_keys(userName)
      passWInput.clear()  
      passWInput.send_keys(password)
      checkbox = driver.find_element(By.XPATH, '//*[@id="pane-second"]/div/div[6]/label/span/span')
      checkbox.click()
      button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.el-button.el-button--primary.login-btn"))
      )
      button.click()
      time.sleep(1)
      loginButton = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[./span[text()="签到 "]]'))
      )
      loginButton.click()
      success = False
      while not success:
        # 使用 XPath 定位到目标 img 元素
        img_element = wait.until(
          EC.presence_of_element_located((By.XPATH, '//div[@class="verify-img-panel"]//img'))
        )
        back_url_value = img_element.get_attribute("src")
        backImage = url_to_imageBytes(back_url_value)
        
        img_element = wait.until(
          EC.presence_of_element_located((By.XPATH, '//div[@class="verify-sub-block"]//img'))
        )
        tar_url_value = img_element.get_attribute("src")
        tarImage = url_to_imageBytes(tar_url_value)
        # 识别
        det = ddddocr.DdddOcr(ocr=False,det=False,use_gpu=False,show_ad=False,beta=True)
        result0 = det.slide_match(tarImage, backImage)
        # result1 = det.slide_comparison(tarImage, backImage)
      
        print(f"******************{result0}****************")
        # print(f"******************{result1}****************")
        
        slideBar = driver.find_element(By.CLASS_NAME, "verify-bar-area")
        barWidth = slideBar.rect["width"]
        imageWidth = get_image_width(backImage)
        imageScale = barWidth / imageWidth
        
        startPosiX = result0.get("target_x")
        tarPoxiX = result0.get("target")[0]
        offsetX = (tarPoxiX - startPosiX) * imageScale
        slider = driver.find_element(By.XPATH, '//div[@class="verify-move-block"]')
        action = ActionChains(driver)
        action.click_and_hold(slider)
        # ofTimes = 10
        # oneOffset = result0.get("target")[0] / ofTimes
        # for _ in range(ofTimes):
        #     # action.move_by_offset(xoffset=oneOffset, yoffset=0)
        #     time.sleep(0.1)
        action.move_by_offset(xoffset=offsetX, yoffset=0)
        action.release().perform()
        target_url = "https://link-ai.tech/api/captcha/check"
        # 等待返回结果
        WebDriverWait(driver, 10).until(
            lambda d: any(req.url == target_url for req in d.requests)
        )
        for request in driver.requests:
          if request.url == target_url and request.response:
              status_code = request.response.status_code
              response_body = request.response.body.decode('utf-8')
              parsed_data = json.loads(response_body)
              if parsed_data.get("repData") is not None:
                  success = parsed_data.get("repData").get("result")
                  if success:
                      print("验证码输入成功")
                  else:
                      print("验证码输入失败,重试")
              break
      driver.save_screenshot('temp1.png')          
  finally:
      print("*****final******")
      if driver is not None:
          driver.quit()

