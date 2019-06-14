# ĐỌC BÁO CRAWLER (PYTHON) 
Framework quét dữ liệu hỗ trợ render javascript và quét đa luồng  

Author: hailoc12  
Email: danghailochp@gmail.com  
Facebook: https://www.facebook.com/danghailochp

# Giới thiệu:  
Đọc Báo Crawler là phần lõi quét dữ liệu cuả dự án [Theo Dõi Báo Chí](https://github.com/hailoc12/docbao) được tác giả đóng gói và đơn giản hoá thành một thư viện và template, nhằm giúp các project trong lĩnh vực Machine Learning, Data Science nhanh chóng xây dựng được phần lõi quét dữ liệu phục vụ dự án.  

Mã nguồn cuả Đọc Báo Crawler đã được xây dựng và test liên tục trong 1 năm rưỡi qua, và có thể hoạt động ổn định trong môi trường production (xem thêm demo quétsong song 35 trang báo sử dụng 10 trình duyệt Firefox cùng lúc tại https://www.youtube.com/watch?v=Y6fl9j6DY1M và website hiển thị dữ liệu đã quét của dự án Theo Dõi Báo Chí tại https://theodoibaochi.com)   

Sử dụng Đọc Báo Crawler, các dự án mới tránh sẽ tránh được rất nhiều vấn để ẩn trong bài toán quét dữ liệu. Một vài vấn đề thường gặp nhất bao gồm:  
- Xếp thời gian quét ngẫu nhiên để tránh bị website block  
- Render javascript để lấy được dữ liệu từ các trang sử dụng Ajax  
- Lấy dữ liệu từ các trang đòi hỏi login, ví dụ Facebook  
- Tự động chặn quảng cáo, chặn flash, CSS để giảm băng thông và tăng tốc độ lấy dữ liệu  
- Xử lý các vấn đề liên quan tới cài đặt và resource leak khi sử dụng selenium +firefox  
- Phân bố job và phối hợp nhiều browser tham gia quét đa luồng để tăng hiệu suất cuả toàn hệ thống  

Hy vọng Đọc Báo Crawler sẽ nhận được sự ủng hộ từ các project data science trong nước và quốc tế. Để tìm hiểu việc sử dụng Đọc Báo Crawler in production với một số tính năng cao cấp hơn như timeout, lọc dữ liệu quét trùng lặp, sử dụng cấu hình quét khác nhau cho từng page...mời xem thêm dự án [Theo Dõi Báo Chí](https://github.com/hailoc12/docbao) hoặc liên hệ trực tiếp với tác giả theo contact ở trên.  

# Vì sao không dùng Scrapy ?  

Scrapy là một framework phổ biến khi nhắc tới việc quét dữ liệu sử dụng Python. Tuy nhiên có một số lý do nên dùng Đọc Báo Crawler thay vì Scrapy như sau:  

1. Kiến trúc của Scrapy rất phức tạp và cứng, nên khó tích hợp vào các dự án khác. Trong khi đó Đọc Báo Crawler đơn giản chỉ là một function và có thể tích hợp vào bất kì phần nào cuả dự án.  

2. Để render javascript với scrapy, phải cài đặt thêm middleware. Điều này làm tăng thời gian tìm hiểu thư viện này, đồng thời tạo ra nhiều lỗi khó xử lý.  

3. Do kiến trúc phức tạp, việc debug lỗi, và tinh chỉnh tính năng với Scrapy là rất khó khăn. Trong khi đó Đọc Báo Crawler được tác giả xây dựng từ đầu, và có thể kiểm soát toàn bộ mã nguồn.  

4. Scrapy vốn được thiết kế để quét sâu một website, thay vì quét nhiều website cùng lúc. Trong khi đó, Đọc Báo Crawler được thiết kế để dễ dàng quét một trang, cũng như nhiều trang cùng lúc. 

# Cài đặt và sử dụng Đọc Báo Crawler  

## 1. Cài đặt  

Cài đặt Đọc Báo Crawler như sau (trên Ubuntu)  

~~~
cd ~
git clone https://github.com/hailoc12/docbao_crawler  
cd docbao_crawler  
bash install.sh  

~~~  

Đọc Báo Crawler sẽ tự cài đặt các lib cần thiết cùng với Firefox browser, Geckodriver  

## 2. Sử dụng  

Khi cần quét một trang, bạn chỉ cần gọi hàm read_url_source() từ module lib/utils.py  

Hàm này có cú pháp như sau:  

~~~  
def read_url_source(url, webconfig,_firefox_browser=BrowserWrapper())

function 
--------
trả về string chưá HTML source code cuả trang mà tham số url dẫn tới. Trang có thể sử dụng Ajax để load dữ liệu hoặc yêu cầu login  

input
-----
- url: link tới trang cần quét  
- webconfig: object cuả lớp WebConfig (trong lib/config.py) chứa thông tin cấu hình để quét trang url. Một số cấu hình quan trọng nhất là:  
   + 'use_browser': sử dụng Firefox browser để quét thay cho phương thức request thông thường  
   + 'browser_fast_load': kích hoạt extension adblock, chặn flash, chặn css để load trang nhanh khi dùng browser  
   + 'browser_profile': sử dụng Firefox profile (đã cài đặt trước thông qua việc chạy file setup_browser.sh) để truy cập các trang cần login  
   + 'display_browser': tắt chế độ headless cuả Browser để dễ debug hơn    
- _firefox_browser: sử dụng một browser đã được instantiate từ cuộc gọi tới read_url_source() lần trước để sử dụng tiếp trong lần quét này.  

output
------
Thành công: trả về string chứa toàn bộ HTML source cuả trang  
Thất bại: trả về None (do lỗi timeout, mất mạng...)  
Trong mọi trường hợp, _firefox_browser sẽ trả về reference tới browser được sử dụng trong cuộc gọi hàm để tái sử dụng, hoặc kill  
~~~  

## 3. Ví dụ   

Đọc Báo Crawler cung cấp sãn 3 file ví dụ, tương ứng với 3 trường hợp quét điển hình. Các bạn có thể sử dụng các file này làm boilerplate cho nhu cầu sử dụng cuả mình  

a. Quét một trang duy nhất, sử dụng trình duyệt hoặc không  

~~~  
python3 crawl_single_page.py  
~~~  

b. Quét một trang cần login (trong ví dụ là Google)  
~~~  
Bước 1: chạy bash setup_browser.sh để mở wizard tạo profile cuả Firefox. Tạo profile mới có tên test_profile. Chú ý chọn path để lưu "user settings, preferences and other user-related data" là ~/docbao_crawler/profiles/test_profile. Sau đó mở Firefox sử dụng profile này, login vào trang bạn cấn quét. Đọc Báo Crawler sẽ sử dụng cookies đã được lưu từ profile này để tự động login vào trang cấn quét  

Bước 2: python3 crawl_login_page.py  
~~~  
c. Quét song song nhiều trang  

python3 crawl_multiprocessing.py  

# Kiến trúc và khả năng mở rộng cuả Đọc Báo Crawler  
Đọc Báo Crawler sử dụng Selenium + Firefox để quét. Class BrowserCrawler (trong lib/browser_cralw.py) cung cấp một lớp trừu tượng hoá để tạo và điều khiển trình duyệt Firefox. Hàm read_url_source() (lib/utils.py) cung cấp giao diện đơn giản để thao tác với class BrowserCrawler thông qua cấu hình quét được cung cấp bởi một đối tượng WebConfig.  

Với các dự án cần mở rộng tính năng cuả Đọc Báo Crawler (ví dụ cần phải click vào một số button trước khi get được trang cần quét), có thể chỉnh sửa trực tiếp vào class BrowserCrawler và function read_url_source(). Việc mở rộng này là tương đối đơn giản, chỉ cần có một chút kiến thức về điểu khiển browser thông qua thư viện Selenium    

Mọi ý tưởng và đóng góp cải tiến Đọc Báo Crawler đều được hoan nghênh và mong đợi. Các phản hồi xin liên hệ tới tác giả theo thông tin ở đầu file README  



