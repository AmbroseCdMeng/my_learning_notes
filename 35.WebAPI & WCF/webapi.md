
# WebAPI
## WebAPI 简介

> WebAPI：(Web Application Programming Interface：网络应用程序接口)
>
> 是一个可以对接各种客户端（浏览器、移动设备），构建 http 服务的框架。是 .net 技术体系下分布式开发的首选技术。与 WebService 和 WCF 相比较，更加的轻量级，传输效率更高。
>

## RESTful 风格

WebAPI 的设计遵循了 RESTful 风格。

> RESTful 是一种软件架构设计风格，提供了一组设计原则和约束条件，基于该风格设计的软件可以更简洁、有层次，更易于实现缓存等机制。

RESTful 设计风格主要原则有：
 
1. 使用 URL 表示资源。

    所谓资源，就是我们希望作为 API 实体呈现的一部分。每个资源都用独一无二的 URL 来表示。

2. 使用 HTTP 协议规范。（GET/POST/PUT/DELETE）

    也就是说，客户端的任何请求都包含一个 URL 和一个 HTTP 请求方法。我们需要遵循这种协议规范来使代码风格更加清晰，可读性更高，同时也方便快速的定位操作。

## 使用 Visual Studio 创建 WebAPI 项目

1. 新建 Web 项目
    ![img01](./img/2019-07-21_112929.png)

2. 选择 WebAPI 模板
    ![img01](./img/2019-07-21_112939.png)

## WebAPI 和 MVC 的区别

> 新建 WebAPI 项目，会发现其 Controller 目录下生成两个控制器（HomeController、ValuesController）

- **HomeController:**
    
    MVC 的控制器，继承了 Controller

- **ValuesController**

    WebAPI 的控制器，继承了 APIController

MVC 的作用是构建网站，重点体现在数据的获取与页面的呈现。默认是通过 Action 的名称来表达动作。

WebAPI 的作用是提供数据访问接口，重点体现在数据的提供与获取。默认是通过 Http 请求动词来定位表达动作。

## WebAPI 的数据访问

### 通过 URL 直接访问

1. 新建一个 WebAPI 控制器，命名为 UserController

    ![img01](./img/2019-07-21_113951.png)
    ![img01](./img/2019-07-21_114326.png)

    添加一个 Get 方法，如下：

    ```cs
    namespace WebAPIService.Controllers
    {
        public class UserController : ApiController
        {
            public String Get() {
                return "Hello WebAPI";
            }
        }
    }
    ```

    启动项目，在浏览器中输入 http://localhost:59465/api/User

    ![img01](./img/2019-07-21_114750.png)

    > 可以发现与 MVC 模式的不同，只指定了控制器名称 User，并没有指定 Action 的名称，为什么会访问到 Get() 方法并返回数据呢？

    - 这就是刚才上面提到，WebAPI 默认是通过 Http 请求动词来定位表达动作的。因为通过 URL 访问，没有指定 Http 请求动词，默认的请求类型就是 GET，所以，只会访问 Get 方法或者以 Get 为前缀的方法。

    > 那如果 Get 方法重载呢？

    修改代码，如下：
    ```cs
    namespace WebAPIService.Controllers
    {
        public class UserController : ApiController
        {
            public String Get() {
                return "Hello WebAPI";
            }

            public String Get(int id) {
                return "Hello WebAPI" + id;
            }
        }
    }
    ```

    启动项目，在浏览器中输入 http://localhost:59465/api/User

    ![img01](./img/2019-07-21_114750.png)

    在浏览器中输入 http://localhost:59465/api/User?id=100
    或者 http://localhost:59465/api/User/100

    ![img01](./img/2019-07-21_115949.png)

    > 可以看到，当 Get 方法重载时，会根据 url 中传参情况来自动调用合适的 Get 方法。那如果同时拥有多个 Get 为前缀的方法呢？

    修改代码，如下：

    ```cs
    namespace WebAPIService.Controllers
    {
        public class UserController : ApiController
        {
            public String Get() {
                return "Hello WebAPI";
            }

            public String Get(int id) {
                return "Hello WebAPI" + id;
            }

            public String GetUserName() {
                return "MCD";
            }
        }
    }
    ```
    启动项目，在浏览器中输入 http://localhost:59465/api/User

    ![img01](./img/2019-07-21_120312.png)

    > 可以看到，请求报错，提示：找到多个匹配的操作。这种问题该如何解决？就需要用到自定义路由规则。稍后会详解。

### 通过 ajax 请求访问

在 MVC 控制器 HomeController 下新建一个页面，用来发送 ajax 请求获取 API 控制器 UserController 下的数据。（需要进入 JQuery ）

- GET 请求（无参）
  
    Index.cshtml 主要代码如下：
    ```html
    <div>
        <div id="webapi"></div>
    </div>
    <script>
        $.ajax({
            url: '/api/User',
            data: {},
            type: 'GET',
            success: function (res) {
                $('#webapi').html(res);
            }
        })
    </script>
    ```
    UserController 主要代码如下：
    ```cs
    public String Get() {
        return "Hello WebAPI";
    }
    public String Get(int id) {
        return "Hello WebAPI" + id;
    }
    ```

    启动项目，访问 http://localhost:59465/

    ![img01](./img/2019-07-21_122253.png)


- GET 请求（基本参数）
    Index.cshtml 主要代码修改如下：

    ```js
    $.ajax({
            url: '/api/User',
            data: {id: 120},
            type: 'GET',
            success: function (res) {
                $('#webapi').html(res);
            }
        })
    ```
    启动项目，访问 http://localhost:59465/
    ![img01](./img/2019-07-21_122622.png)

- GET 请求（实体参数）
    在 Models 目录下添加一个 User.cs，内容如下：
    ```cs
    namespace WebAPIService.Models {
        public class User {
            public int UserID { get; set; }
            public string Username { get; set; }
        }
    }
    ```

    UserController 中修改如下：
    ```cs
    public class UserController : ApiController
    {
        public String Get(User user) {
            return user.Username;
        }
    }
    ```

    Index.cshtml 中修改如下：

    ```js
    $.ajax({
            url: '/api/User',
            data:{'UserId':'1680502', 'UserName':'MCD'},
            type: 'GET',
            success: function (res) {
                $('#webapi').html(res);
            }
        })
    ```
    启动项目，尝试访问 http://localhost:59465/
    ![img01](./img/2019-07-21_124304.png)

    > 请求报错！！！
    
    > 为何会后台代码报错？
    - 原因，实体参数传递失败，导致 user 的值 为 null。
    - 解决，Get 请求传递实体参数，需要在参数前加上 FromUri 特性声明。

    修改 UserController 中代码如下：
    ```cs
    public class UserController : ApiController
    {
        public String Get([FromUri]User user) {
            return user.Username;
        }
    }
    ```
    启动项目，访问 http://localhost:59465/
    ![img01](./img/2019-07-21_124441.png)

- POST 请求（无参）

    UserController 中添加一个 PostUser 方法
    ```cs
    public class UserController : ApiController
    {
        public String PostUser() {
            return "Post";
        }
    }
    ```
    index.cshtml 中修改 ajax 请求类型为 POST
    ```js
    $.ajax({
        url: '/api/User',
        data: {},
        type: 'POST',
        success: function (res) {
            $('#webapi').html(res);
        }
    })
    ```
    启动项目，访问 http://localhost:59465/
    ![img01](./img/2019-07-21_125110.png) 

- POST 请求（基本参数）
    UserController 中修改如下
    ```cs
    public class UserController : ApiController
    {
        public String PostUser(int userId) {
            return userId.ToString();
        }
    }
    ```
    index.cshtml 中修改 ajax 请求
    ```js
    $.ajax({
        url: '/api/User',
        data: { userId: '1680502'},
        type: 'POST',
        success: function (res) {
            $('#webapi').html(res);
        }
    })
    ```
    启动项目，访问 http://localhost:59465/
    
    请求报错！！！

    ![img01](./img/2019-07-21_125433.png)
    
    > 原因：POST 基本参数接收失败，找不到匹配的操作
    >
    > 解决：POST 请求传递基本参数，需要在参数前加上 FromBody 特性声明。

    修改 UserController 如下：
    ```cs
    public class UserController : ApiController
    {
        public String PostUser([FromBody]int userId) {
            return userId.ToString();
        }
    }
    ```
    启动项目，访问 http://localhost:59465/
    ![img01](./img/2019-07-21_130603.png)

    > 返回的 userId 为 0 ？？？
    >
    > 原因：int 类型的默认值为 0，说明请求虽未报错，但 userId 的值却传递失败
    >
    > 解决：WebAPI 中 Post 传递基本参数，如果只有一个参数，不需要指定参数名，如果多个参数，需要使用动态参数来接收，同时需要修改 contenttype 属性的值为 application/json，contenttype 属性是用来设置发送给服务端的数据格式的，同样还有 dataType 用来设置接收到服务端的数据格式，默认情况下 contenttype 的值为 appliction/x-www-form/urlencoded，这种格式下的参数形式与 Get 请求中的 url 格式相同，只不过 Post 中不是存放在 url 地址中而已。

    修改 Index.cshtml 如下：
    ```js
    $.ajax({
        url: '/api/User',
        data: { '': '1680502'},
        type: 'POST',
        success: function (res) {
            $('#webapi').html(res);
        }
    })
    ```

    启动项目，访问 http://localhost:59465/
    ![img01](./img/2019-07-21_131053.png)


    多个基本参数时：
    修改 Index.cshtml 如下：
    ```js
    $.ajax({
        url: '/api/User',
        data: JSON.stringify({ userId: 1680502, userName:'MCD' }),
        type: 'POST',
        contentType: "application/json",
        success: function (res) {
            $('#webapi').html(res);
        }
    })
    ```
    修改 UserController 如下：
    ```cs
    public class UserController : ApiController
    {
        public String PostUser(dynamic user) {
            return user.userId + ">>>" + user.userName;
        }
    }
    ```
    启动项目，访问 http://localhost:59465/
    ![img01](./img/2019-07-21_131924.png)
    


- POST 请求（实体参数）

    修改 Index.cshtml 如下：

    ```js
    $.ajax({
        url: '/api/User',
        data: { userId: 1680502, userName:'MCD' },
        type: 'POST',
        success: function (res) {
            $('#webapi').html(res);
        }
    })
    ```
    修改 UserController 如下：
    ```cs
    public class UserController : ApiController
    {
        public String PostUser([FromBody] User user) {
            return user.UserID + ">>>" + user.Username;
        }
    }
    ```
    启动项目，访问 http://localhost:59465/
    ![img01](./img/2019-07-21_132339.png)

### 通过客户端访问

修改 Home 控制器中 Index 方法如下：

```cs
public ActionResult Index(){

    //1、创建URI
    Uri uri = new Uri("http://localhost:59465");
    //2、创建一个 HttpClient 客户端对象
    HttpClient httpClient = new HttpClient();
    //3、设置要求 WebAPI 返回的数据类型。默认 json
    httpClient.DefaultRequestHeaders.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));

    //4、设置 HttpClient 客户端获取资源数据的地址
    httpClient.BaseAddress = uri;

    //5、发送一个 get 方法的请求
    var PushAction = httpClient.GetAsync("api/User");

    //6、获取 get 方法请求之后返回的数据 
    var responseResult = PushAction.Result;

    //7、判断返回的数据状态
    if(responseResult.StatusCode == System.Net.HttpStatusCode.OK){
        //Content:获取 HTTP 响应消息的内容
        //ReadAsStringAsyunc():以异步操作将HTTP内容写入流
        //Result:获取此 System.Threading.Tasks.Task<TResult> 的结果值
        var result = responseResult.Content.ReadAsStringAsync().Result;
        //反序列化
        var list = JsonConvert.DeserializeObject<List<User>> (result);

        //8、释放资源
        httpClient.Dispose();

        return View(list);
    }else{
        httpClient.Dispose();
    }
    return View();
}

```
> 如果遇到服务器提交了协议冲突问题，可以在客户端配置文件中加入如下配置解决：

```
<system.net>
    <settings>
      <httpWebRequest useUnsafeHeaderParsing="true"/>
    </settings>
  </system.net>
```


### 补充 1 -- 常用特性：
  - 如果方法名不遵守 Http 请求动词为前缀等规则，也可以在方法上加上 HttpPost、HttpGet 等特性声明来指定请求类型。如 [HttpPost]、[HttpGet]
  - 如果某方法需要支持多种请求类型，可以在方法上加上 AcceptVerbs 特性声明来执行多个请求类型。如：[AcceptVerbs["Get", "Post"]
  - 如果需要重写 Action 的名称，可以使用 ActionName 特性声明。如：[ActionName("DeleteUser")]
  - 如果某方法不需要参与路由匹配可以使用 NoAction 特性声明

### 补充 2 -- Http 协议规范：
- GET ：用于从服务器端获取数据。类似于 Select，不应该对服务器端的数据产生任何影响
- POST：用于向服务器端增加数据，类似于 Insert，会对服务器端数据产生影响
- PUT： 用于向服务器端更新数据，类似于 Update，会对服务端数据产生影响
- DELETE：用于向服务器端删除数据，类似于 Delete， 会对服务器端数据产生影响
- OPTION：用于向服务器端发送探测请求，获取服务器是否允许执行某种类型请求。

    作为最常用的两种请求方式 Get 和 Post，很多情况下都会被混用。其实它们本质上都作为 TCP 链接，并无差别。但是因为一些其他的限制于规范，导致在应用过程中体现出一些不同之处。
    
    - 其最大的区别在于数据的传输方式：Get 请求方式下，浏览器将请求头(http Headers)与数据(data)同时发送出去，然后服务器返回响应200；Post 请求下，浏览器会先发送请求头(http Headers)，等待服务器响应 100(continue) 之后，再发送数据(data)，然后等待服务器响应200
    - Get 请求的参数是直接附加在 url 后的，明文显示在 url 连接中；Post 请求的参数是放置在 Http 包体中。
    - Get 因为请求参数附加在 url 中，而 url 的长度理论上也是没有限制的，但是因为特定环境（浏览器、操作系统）的影响（IE 浏览器的 url 长度限制为 2083 字节，2K），所以导致 Get 请求的参数大小也有限制。同样 Post 的参数大小理论也没有限制，但是由于环境（服务器）的影响，也会有一定的限制（IIS6默认100K），所以，相对而言，可以说 Post 请求传递参数的大小几乎没有限制。
    - Get 请求会被主动缓存，相对安全性较低；Post 请求默认不缓存，如需缓存需要手动设置
    - Get 请求只支持 URL 编码，所以也只能传递 ASCII 字符的参数；Post 请求支持多种编码格式，参数类型无限制。

## 路由规则

- MVC 的路由

    在 MVC 里面，默认路由机制是通过 url 路径去匹配对应的 action 方法，如 Home/Index 、 Home/GetUser
    
    在 MVC 里面，默认路由位于 APP Start 文件夹下的 RouterConfig.cs 中

- WebAPI 的路由

    在 WebAPI 的默认路由是通过 HTTP 的方法（Get/Post/Put/Delete）去匹配对应的 action，也就是说 webapi 的默认路由不需要指定 action 的名称；
    
    在 WebAPI 里面，默认路由位于 App Start 文件夹下的 WebApiConfig.cs 中

### WebAPI 的路由约束

```cs
config.Routes.MapHttpRoute(
    name: "DefaultApi",
    routeTemplate: "api/{controller}/{id}",
    defaults: new { id = RouteParameter.Optional },
    constraints:new { id=@"\d+"}  //约束正则(指定 id 只能为 数字)
);
```

启动项目，访问 http://localhost:59465/api/User/100
![img01](./img/2019-07-21_133007.png)

访问 http://localhost:59465/api/User/100px
![img01](./img/2019-07-21_133028.png)

### WebAPI 自定义路由
```cs
config.Routes.MapHttpRoute(
    name: "MyApi",
    routeTemplate: "myapi/{controller}/{action}/{id}",//加入 action 占位符后，就可以解决前面遇到的多个GET请求匹配问题
    defaults: new { id = RouteParameter.Optional }
);
```

修改 UserController 如下：

```cs
 public class UserController : ApiController
{
    public String Get() {
        return "Hello WebAPI Get";
    }

    public String GetUser() {
        return "Hello WebAPI GetUser";
    }
}
```
启动项目，访问 http://localhost:59465/
![img01](./img/2019-07-21_133448.png)


### 特性路由(新版本默认已经配置)

WebApiConfig.cs 文件中加入
```cs
config.MapHttpAttributeRoutes();
```

Global.asax 文件中加入
```cs
GlobalConfiguration.Configure(WebApiConfig.Register);
```

使用特性路由

修改 UserController 如下：
```cs
public class UserController : ApiController
{
    [Route("RouteUser/{uid}/GetName")]
    public String GetUserName(int uid) {
        return "特性路由测试" + uid;
    }
}
```

启动项目，访问 http://localhost:59465/RouteUser/123/GetName
![img01](./img/2019-07-21_134323.png)


## 跨域访问

1. 新建一个 MVC 项目。命名 WebAPIClient，作为客户端。
2. 启动服务端 WebAPIService
3. 在 WebAPIClient 的 Home/Index 页面下引入 jquery 文件，使用 ajax 请求调用服务端接口

    ```js
    $.ajax({
            url: 'http://localhost:59465/RouteUser/1680502/GetName',
            data: {},
            type: 'GET',
            success: function (res) {
                $('#webapi').html(res);
            }
        })
    ```

    请求报错！！！

    ![img01](./img/2019-07-22_003921.png)

    > 原因：跨域请求不被允许
    >
    > 解决：配置服务端文件，允许跨域请求。
    
    在 webconfig 文件中
    ```xml
    <system.webServer>
    ...
        <httpProtocol>
        <customHeaders>
            <!-- 响应类型：表明服务器支持的所有跨域请求的方法 -->
            <add name="Access-Ｃontrol-Allow-Methods" value="GET,POST,PUT,DELETE,OPTIONS"/>
            <!-- 响应头设置(Content_-Type)： application/x-www-form-urlencoded、multipart/form-data、text/plain -->
            <add name="Access-Control-Allow-Headers" value="x-requested-with,content-type"/>
            <!-- 允许跨域访问的域名 -->
            <add name="Access-Control-Allow-Origin" value="*"/>
        </customHeaders>
        </httpProtocol>
    ...
    </system.webServer>
    ```

    刷新客户端页面，重新发送 ajax 跨域请求。

    ![img01](./img/2019-07-22_004958.png)