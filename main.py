from DrissionPage import ChromiumPage, ChromiumOptions
import ddddocr
import time
import json
from imageUtil import url_to_imageBytes, get_image_width

userName = "xxxxx"
password = "xxxxx"

debugMode = False
checkUrl = 'api/captcha/check'

if __name__ == "__main__":
    myUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    co = ChromiumOptions()    # .incognito() # 隐身模式
    co.set_argument('--no-sandbox', '--disable-extensions')
    co.set_argument('--disable-blink-features=AutomationControlled')
    co.set_user_agent(myUserAgent)
    
    if not debugMode:
        co.headless()  # 无头模式
        co.no_imgs(True)  # 禁用图片
        co.set_pref('profile.managed_default_content_settings.stylesheet', 2)  # 禁用CSS

    page = ChromiumPage(addr_or_opts=co)
    try:
        page.get("https://link-ai.tech/console/account")
        page.listen.start(checkUrl) 
        try: 
            # '#'号id选择器
            page.ele('#tab-second', timeout=3).click()
            # 输入账号密码
            inputs = page.eles('tag:input@class:el-input__inner', timeout=3)
            inputs[0].input(userName)
            inputs[1].input(password)
            # 复选框处理
            checkbox = page.ele('.el-checkbox__original', timeout=3)
            # checkbox.input("true") 
            checkbox.click(by_js=True) 
            # 登录
            loginButton = page.ele('.el-button el-button--primary login-btn', timeout=3)
            loginButton.click(by_js=True) 
        except Exception as e:
            print("无登录页,已有cookie登录")
        finally:
            # 签到
            parent = page.ele('.edit-btn', timeout=5)
            btn = parent.ele('css:.el-button.is-plain', timeout=3)
            btn.click(by_js=True)   
            success = False
            while not success:
                # 获取验证码图片
                back_img = page.ele('xpath://div[@class="verify-img-panel"]//img').attr('src')
                tar_img = page.ele('xpath://div[@class="verify-sub-block"]//img').attr('src')
                
                # 识别逻辑（保持不变）
                backImage = url_to_imageBytes(back_img)
                tarImage = url_to_imageBytes(tar_img)
                det = ddddocr.DdddOcr(ocr=False, det=False, use_gpu=False, show_ad=False, beta=True)
                result0 = det.slide_match(tarImage, backImage)
                
                # 计算滑动距离
                slide_bar = page.ele('.verify-bar-area', timeout=3)
                bar_width = slide_bar.run_js('return this.offsetWidth')
                image_width = get_image_width(backImage)
                image_scale = bar_width / image_width
                offsetX = (result0["target"][0] - result0["target_x"]) * image_scale
                
                # 滑动操作
                slider = page.ele('.verify-move-block', timeout=3)
                slider.drag(offsetX, 0, duration=0.5)  # 使用内置滑动方法
                
                # 检查验证结果（通过监听响应）
                # step 默认阻塞模式
                for packet in page.listen.steps(timeout=3):
                    if checkUrl in packet.url:
                        recieved = True
                        response_body = packet.response.body
                        # print("response_body:", response_body)
                        # parsed_data = json.loads(response_body)
                        if response_body.get('repData', {}) is not None:
                            success = response_body.get('repData', {}).get('result', False)
                        if success:
                            print("验证通过")
                        else:
                            print("验证失败，重试")
                        break
   
            page.get_screenshot('temp1.png', full_page=True)
        
    finally:
        print("*****final******")
        page.listen.stop() 
        page.quit()