---
title: Windows系统初探MongoDB的基础使用
date: 2020-04-14 16:55:06
tags: [MongoDB, 数据库, 程序员]
---

![](https://image-static.segmentfault.com/409/895/4098956202-5e957aeebe442_articlex)

### MongoDB是什么？

> MongoDB 是由C++语言编写的，是一个基于分布式文件存储的开源数据库系统。MongoDB 将数据存储为一个文档，数据结构由键值(key=>value)对组成。MongoDB 文档类似于 JSON 对象。字段值可以包含其他文档，数组及文档数组。

### 下载安装

MongoDB 提供了可用于 32 位和 64 位系统的预编译二进制包，你可以从MongoDB官网下载安装，MongoDB 预编译二进制包下载地址：
[https://www.mongodb.com/download-center/community](https://www.mongodb.com/download-center/community)

我的MongoDB是安装在D:\mongodb目录下，安装好后，进入到安装目录D:\mongodb\data下，新建一个数据库目录，例如db

<!-- more -->

### mongodb服务端启动

#### 绝对路劲的方式启动

打开命令行工具，这里我推荐一下[Cmder](https://cmder.net/)命令行工具，我一直在用，打开后，输入`D:\mongodb\bin\mongod --dbpath D:\mongodb\data\db`回车执行

#### mongod命令的方式启动

配置了bin目录的Path路径，可以直接用mongod命令启动服务器，执行`mongod --dbpath D:\mongodb\data\db`或者在data目录下执行`mongod --dbpath .\db`

#### 配置bin的Path路径

为了启动mongodb方便，将mongod.exe路径加入环境变量，位置：**计算机->属性->高级系统设置->环境变量**,在系统变量的Path里，在末尾加上安装MongoDB的bin目录，记得加英文分号‘;’。全部确定保存后，重新打开命令行窗口，就可以在任何地方都能用到mongod命令以及bin目录下的其他命令了

### 客户端连接

在之前启动了服务器后，千万不要关闭服务端的命令行窗口，需要再重新打开一个命令行窗口，在任意目录下输入mongo即可启动客户端（如果遇到“'mongo'不是内部或外部命令，也不是可运行的程序或批处理文件。”，请配置上面的Path路径）；如果你就是不想配置Path路径，那你直接到你安装目录的bin目录下，双击mongo.exe打开也能直接连接客户端


### MongoDB 概念解析

在mongodb中基本的概念是文档、集合、数据库

- 数据库：一个mongodb中可以建立多个数据库；MongoDB的默认数据库为"db"，该数据库存储在data目录中。使用show dbs，可以查看全部数据库
- 集合：集合就是 MongoDB 文档组，类似于RDBMS中的表格。集合存在于数据库中，集合没有固定的结构，这意味着你在对集合可以插入不同格式和类型的数据。使用`show collections`，可以查看当前数据库实例下的全部集合
- 文档：文档是一组键值(key-value)对(即 BSON)。MongoDB 的文档不需要设置相同的字段，并且相同的字段不需要相同的数据类型。使用`db.collection.find()`命令，可以查看collection集合下的全部文档

### 数据库（db）

初次连接客户端，使用db查看，默认使用的是test数据库，再使用show dbs查看全部数据库，并使用use命令切换数据库，例如使用use admin切换到admin数据库
```
> db
test
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
school  0.000GB
test    0.000GB
> use admin
switched to db admin
```

#### 新建数据库

新建数据库的语法为：`use databaseName`，也就是和切换数据库是一样的，如果切换的数据库不存在，则创建新的数据库，例如需要使用`use order`新建一个数据库order，但是使用`show dbs`查看并没有发现新建的数据库，也就是空集合的数据库不会显示出来，则需要向order中随便插入一个文档就能看到了，例如我们执行`db.info.insert({'name':'张三','note':'hello world'})`向info集合中插入一条文档，再使用`show dbs`就能看到order数据库了
```
> use order
switched to db order
> db
order
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
school  0.000GB
test    0.000GB
> db.info.insert({'name':'张三','note':'hello world'})
WriteResult({ "nInserted" : 1 })
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
order   0.000GB
school  0.000GB
test    0.000GB
```

#### 删除数据库

可以使用`db.dropDatabase()`删除当前数据库，再使用`show dbs`查看当前数据库是否删除，可以看到school已经不存在了（好奇的人，这时候也许会问：我在当前数据库下删除其他数据库可以吗？我试了下，好像不行，报错了……）
```
> use school
switched to db school
> db
school
> db.dropDatabase()
{ "dropped" : "school", "ok" : 1 }
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
order   0.000GB
test    0.000GB
```

### 集合（collection）

#### 创建集合

创建集合的语法为`db.createCollection(name, options)`，第一个参数name是必传的集合名，第二个options是指定有关内存大小及索引的选项的可选参数，例如，我们使用命令`db.createCollection('goods')`在order数据库下新建一个goods集合，然后使用`show collections`或`show tables`命令查看该数据库下的文档
```
> use order
switched to db order
> db.createCollection('goods')
{ "ok" : 1 }
> show collections
goods
info
> show tables
goods
info
```

#### 能不能不用预先创建集合？

当然是可以的，其实在MongoDB中，我们不需要先创建集合，因为当你插入文档后，MongoDB会自动创建该集合，例如，我们使用`db.user.insert({'name':'lisan','age':23,'sex':'w'})`在order数据库中创建user集合并插入一条文档
```
> show tables
goods
info
> db.user.insert({'name':'lisan','age':23,'sex':'w'})
WriteResult({ "nInserted" : 1 })
> show collections
goods
info
user
```

#### 删除集合

创建了集合，那么肯定就需要删除多余的集合，删除集合的语法为`db.collectionName.drop()`，例如，我们使用`db.user.drop()`删除刚刚创建的user集合
```
> db.user.drop()
true
> show collections
goods
info
```

**友情帮助**：对了，可以使用`db.collectionName.help()`查看集合的帮助，例如：`db.goods.help()`

### 文档（document）

#### 插入文档

MongoDB使用insert()方法向集合中插入文档，语法为`db.collectionName.insert(document)`，例如使用`db.goods.insert({'name':'商品名称','price':123,'sale':6})`向goods集合中插入一条数据（当我们插入一条文档的时MongoDB会自动为此文档生成一个_id属性，且_id的值一定是唯一的，默认为objectId()）
```
> db.goods.insert({'name':'商品名称','price':123,'sale':6})
WriteResult({ "nInserted" : 1 })
```

#### 插入文档的其他方法

插入文档，还是可以使用`db.collectionName.insertOne(document)`插入一条或者使用`db.collectionName.insertMany(document)`插入多条，insertOne()的使用和insert()一样的，document都是一个json对象；insertMany()插入多条时，document是多个json对象的数组，示例如下：
```
> db.goods.insertOne({'name':'商品名称6','price':19,'sale':9}))))

        "acknowledged" : true,
        "insertedId" : ObjectId("5e953450aabbbfa8f930a967")
}
> db.goods.insertMany([{'name':'商品名称88','price':18,'sale':1},{'name':'商品名称99','price':99,'sale':99}])))

        "acknowledged" : true,
        "insertedIds" : [
                ObjectId("5e953475aabbbfa8f930a968"),
                ObjectId("5e953475aabbbfa8f930a969")
        ]
}
```

另外，插入文档也可以使用`db.collectionName.save(document)`命令。如果不指定_id字段save()方法类似于insert()方法。如果指定_id字段，则会更新该_id的数据。

#### 更新文档

MongoDB使用update()方法来更新集合中的文档，语法如下：
```
db.collectionName.update(
   <query>,
   <update>,
   {
     upsert: <boolean>,
     multi: <boolean>,
     writeConcern: <document>
   }
)
```

前面，我们再goods集合中插入了一条`{'name':'商品名称6','price':19,'sale':9}`的文档，现在我们更新这个文档，把名称 name=商品名称6 的价格 price 改为91，则更新命令为`db.goods.update({'name':'商品名称6'}, {$set:{'price':91}})`，更新前后对比发现确实变了
```
> db.goods.find()
{ "_id" : ObjectId("5e95322caabbbfa8f930a965"), "name" : "商品名称", "price" : 123, "sale" : 6 }
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称6", "price" : 19, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a968"), "name" : "商品名称88", "price" : 18, "sale" : 1 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
> db.goods.update({'name':'商品名称6'}, {$set:{'price':91}})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.goods.find()                                       1}})
{ "_id" : ObjectId("5e95322caabbbfa8f930a965"), "name" : "商品名称", "price" : 123, "sale" : 6 }
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称6", "price" : 91, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a968"), "name" : "商品名称88", "price" : 18, "sale" : 1 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
```

也可以通过save()方法通过传入的文档来替换已有文档，必须传入_id的值

#### 部分更新操作符

上面的update命令中，可能你会问\$set那个是什么意思呢？这是操作符，用来指定设置文档某字段的值，还有其他很多更新操作符，下面大概列一下：
- $unset：删除指定字段
- $inc：给一个字段增加指定数值
- $pop：删除数组字段中的第一个或最后一个元素
- $push：向数组中追加一个值
- $pushAll：向数组中追加多个指定值
- $pull：符合条件的值将被删除
- 其他……

#### 其他更新文档说明

另外，update()默认只会更新符合条件的第一条数据，如果需要全部更新，则需要指定multi的值为true，例如下面的数据，我提前把两条文档的price改为18，然后把这两条文档的name改为“商品名称相同”，可以看到执行一次，两条数据都变了
```
> db.goods.find()                                                      e}})
{ "_id" : ObjectId("5e95322caabbbfa8f930a965"), "name" : "商品名称", "price" : 123, "sale" : 6 }
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称6", "price" : 18, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a968"), "name" : "商品名称88", "price" : 18, "sale" : 1 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
> db.goods.update({'price':18}, {$set:{'name':'商品名称相同'}}, {multi: true})
WriteResult({ "nMatched" : 2, "nUpserted" : 0, "nModified" : 2 })
> db.goods.find()                                                       true})
{ "_id" : ObjectId("5e95322caabbbfa8f930a965"), "name" : "商品名称", "price" : 123, "sale" : 6 }
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称相同", "price" : 18, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a968"), "name" : "商品名称相同", "price" : 18, "sale" : 1 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
```

还有，在3.2版本开始，MongoDB还提供了`db.collectionName.updateOne()`更新一个文档，`db.collectionName.updateMany()`更新多个文档，更新单个和update相同，传入前两个参数即可，使用updateMany()更新多个更加方便，不必传入multi为true了

#### 删除文档

MongoDB使用remove()来移除文档，其语法如下
```
db.collectionName.remove(
   <query>,
   {
     justOne: <boolean>,
     writeConcern: <document>
   }
)
```

我们使用remove()来移除goods集合中 name=商品名称 的文档，其命令为`db.goods.remove({'goods': '商品名称'})`
```
> db.goods.remove({'name': '商品名称'}))
WriteResult({ "nRemoved" : 1 })
> db.goods.find()
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称相同", "price" : 18, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a968"), "name" : "商品名称相同", "price" : 18, "sale" : 1 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
```

#### 其他删除文档说明

1. 执行删除操作的时候，默认是删除所有符合条件的数据，如果你想删除指定的最多条数，则在第二个参数传入该限制数字：`db.goods.remove({'goods': '商品名称'}, 2)`，如果你想删除集合的全部文档传入空对象即可，也就是`db.goods.remove({})`

2. remove()方法已经过时了，现在官方推荐使用 deleteOne()删除单个文档 和 delete；Many()删除多个文档，例如删除多个的命令为`db.goods.deleteOne({'goods': '商品名称'})`，删除多个的命令为`db.goods.deleteMany({'goods': '商品名称'})`

#### 查询文档

MongoDB 查询文档使用 find() 方法，其语法为`db.collectionName.find(query, projection)`，两个参数都是可选的（其中query是查询条件，projection是返回字段），啥都不传默认查询全部文档的全部字段
查找goods集合的全部文档，命令为`db.goods.find()`
```
> db.goods.find()
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称相同", "price" : 18, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a968"), "name" : "商品名称相同", "price" : 18, "sale" : 1 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
查找goods集合sale大于6的文档，命令为db.goods.find({'sale': {$gt: 6}})
> db.goods.find({'sale': {$gt: 6}})
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称相同", "price" : 18, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
查找goods集合sale大于6且price小于20的文档，命令为db.goods.find({'sale': {$gt: 6}, 'price': {$lt: 20}})
> db.goods.find({'sale': {$gt: 6}, 'price': {$lt: 20}})
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称相同", "price" : 18, "sale" : 9 }
```

#### 条件操作符说明

从上面的查询命令中，可能有人会注意到，\$gt或者\$lt这是什么意思呢，这是条件操作符，具体部分操作符如下：
- $gt：查找字段值大于指定值的文档
- $lt：查找字段值小于指定值的文档
- $gte：查找字段值大于等于指定值的文档
- $lte：查找字段值小于等于指定值的文档
- $in：查找字段值等于指定数组中的任何值
- $nin：字段值不在指定数组或者不存在
- $or：文档至少满足其中的一个表达式
- $eq：查找字段值等于指定值的文档
- $ne：查找字段值不等于指定值的文档，包括没有这个字段的文档
- 其他……

#### 正则匹配的模糊查询

另外，关于一些模糊查询，MongoDB还支持正则匹配，语法为：`db.collectionName.find({key:/value/})`，例如下面的查询
```
> db.goods.find({'name': /99/}))))
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
> db.goods.find({'name': /相同$/}))
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称相同", "price" : 18, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a968"), "name" : "商品名称相同", "price" : 18, "sale" : 1 }
> db.goods.find({'name': /^商品/})
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称相同", "price" : 18, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a968"), "name" : "商品名称相同", "price" : 18, "sale" : 1 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
```

#### 分页限制查询

我们知道find()查询默认返回符合条件的全部文档，如果想只查询指定条数呢，这时候就需要用到limit()方法了，其语法为`db.collectionName.find().limit(number)`

limit()是返回符合条件的前几条数据，如果我想返回中间的几条数据，该怎么取？这时候同样需要skip()方法来跳过指定数量的记录数，其语法为`db.collectionName.find().limit(number).skip(number)`

上面的goods集合中，我们想跳过前三条获取第四条name为“商品名称99”的数据，其命令为`db.goods.find().limit(1).skip(3)`
```
> db.goods.find().limit(1).skip(3)
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
```

#### 排序查询

在 MongoDB 中使用 sort() 方法对数据进行排序，sort() 方法可以通过参数指定排序的字段，并使用 1 和 -1 来指定排序的方式，其中 1 为升序排列，而 -1 是用于降序排列。排序查找的基本语法为`db.collectionName.find().sort({key:1})`

例如上面的goods集合，我们想查询结果按照sale升序排序，则命令为`db.goods.find().sort({'sale': 1})`
```
> db.goods.find().sort({'sale': 1})
{ "_id" : ObjectId("5e953475aabbbfa8f930a968"), "name" : "商品名称相同", "price" : 18, "sale" : 1 }
{ "_id" : ObjectId("5e95340faabbbfa8f930a966"), "name" : "商品名称1", "price" : 19.99, "sale" : 8 }
{ "_id" : ObjectId("5e953450aabbbfa8f930a967"), "name" : "商品名称相同", "price" : 18, "sale" : 9 }
{ "_id" : ObjectId("5e953475aabbbfa8f930a969"), "name" : "商品名称99", "price" : 99, "sale" : 99 }
```

**温馨提示**：这里需要说明一下，当skip()、limilt()和sort()三个放在一起执行的时候，执行的顺序是先 sort(), 然后是 skip()，最后是显示的 limit()

### 最后说明

到了这里，相信大家对于MongoDB的基础用法都会了，如果需要了解更多，可以查找相关的教程和官方说明，如有说的不对或者不全的，请大家指出，我会及时改正，谢谢。