# 安居客-爬虫范例
> scrapy-anjuke

### 数据库存储-MongoDB

* MONGODB_SERVER = 'localhost'
* MONGODB_PORT = 27017
* MONGODB_DB = 'python'
* MONGODB_COLLECTION：
    * 页面集合：PAGE = 'anjuke_page'
    * 房子集合： HOUSE = 'anjuke_house'

### 数据结构-items

#### PageItem 页面信息
* 页数：page
* 页面路径：page_url
* 房屋路径：house_urls

#### HouseItem 房子信息
* ID：house_id
* 标题：title
* 房屋总价：tolprice
* 房屋户型：mode
* 建筑面积：area
* 房屋单价：price
* 房屋朝向：orientation
* 所在楼层：floor
* 装修程度：decorate
* 建造年代：built
* 房屋类型：house_type
* 房本年限：agelimit
* 配套电梯：elevator
* 唯一住房：only
* 参考月供：budget
* 所属小区：district
* 交通：traffic

### 注意

#### 验证码页面-发生302时，需要验证

[302验证](https://m.anjuke.com/captcha-verify/?callback=shield&from=antispam&serialID=74fa0d90c7197db48626c55f5d4cdf69_668f34e50a7e4e4ebe7e347f976943f5&history=aHR0cHM6Ly9tLmFuanVrZS5jb20vZ3ovc2FsZS9BMTQ3OTQ1OTgxNi8%2FaXNhdWN0aW9uPTIwMSZwb3NpdGlvbj0zMDQma3d0eXBlPWZpbHRlcg%3D%3D)