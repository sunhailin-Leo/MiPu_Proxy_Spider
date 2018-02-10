# 米扑代理爬虫

---

<h3 id="Difficulty">难点</h3>

* 未登陆用户只能看一页的代理IP
* IP的端口都是用图片形式呈现（一种反爬的手段）
* OCR识别上,原图太小.需要放大才能识别

---

<h3 id="Dependency">依赖</h3>

* 软件依赖:
    * tesseract-OCR(OCR的软件，安装方式自行百度)
* Python依赖
    * pytesseract
    * Pillow
    * lxml

---

<h3 id="Env">测试环境</h3>

* Win10 x64
* Python3.4.4
* tesseract-OCR 4.0.0-alpha

---

<h3 id="LastButNotLeast">最后</h3>

* 我这写的是一个工具类,部署好一切东西只要调用就好了（不过没加入多线程, 处理速度稍微有点慢, 因为依赖于OCR的接口）
* 其次没有写验证代理的可用性（想着只是一个调用的方法, 验证代理可用性的方法在开发中肯定会独立出来，所以就没有写了）

* 多线程的之后会改进~ 看看如何提升速度