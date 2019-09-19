# WebAPI

## WebAPI 简介

>API：Application Programming Interface

>WebAPI：可以对接各种客户端（浏览器、移动设备），构建 http 服务的框架。是 .net 技术体系下分布式开发的首选技术。与 WebService 和 WCF 相比较，更加的轻量级，传输效率更高。


## RESTful 风格

> WebAPI 的设计遵循了 RESTful 风格。

RESTful 是一种软件架构设计风格，提供了一组设计原则和约束条件，基于该风格设计的团建可以更简洁、有层次，更易于实现缓存等机制。

RESTful 风格的主要原则：
    
1. 使用 URL 表示资源。所谓资源，就是我们希望作为 API 实体呈现的一部分。每个资源都用独一无二的 URL 来表示。

2. 使用 HTTP 协议规范。（GET/POST/PUT/DELETE）

也就是说，客户端的任何请求都包含一个 URL 和一个 HTTP 请求方法。我们需要遵循这种协议规范来使代码风格更加清晰，可读性更高，同时也方便快速的定位操作。

## 使用 Visual Studio 新建 WebAPI

> ValuesController -- WEBAPI 的控制器，继承了 APIController
> 
> HomeController -- MVC 的控制器，继承了 Controller

## WebAPI 和 MVC 的异同

MVC 主要用来构建网站，重点在于数据的获取与页面的呈现。

WebAPI 主要用来提供数据接口，重点在于数据的获取。

---

MVC 通过 Action 的名称表达动作

WebAPI 通过不同的 Http 请求动词，如 GetValues、PutUsers 来定位要访问的动作

---

WebAPI 非常适合构建移动客户端服务

## 通过 URL 访问 WebAPI

http://localhost:54136/api/Values

没有指定 HTTP 请求类型，默认 GET，所以只会访问 Get 或者 前缀为 Get 的方法

public IEnumerable<string> Get() {...}

---

http://localhost:54136/api/Values/1

GET 传递基本参数

public string Get(int id) {...}

---

GET 方式传递实体参

data:{'Fid':'123', 'Name':'111'},

public string GetProName([FromUri]Food model) {
            return model.FName;
        }

---

POST 方式传基本参
$.ajax ({
    url:'',
    data:Json.stringify{'':'123'},
    type:'POST',
    success:function(){

    }
})

public void PostProName([FromBody]string value,) {}


$.ajax ({
    url:'',
    contentType:'application/json',
    data:Json.stringify({ID:'123', NAME:'text'}),
    type:'POST',
    success:function(){

    }
})



/*动态属性*/
public void PostProName(dynamic pro) {return pro.NAME}


--- 

POST 方式传递实体参

data:{'Fid':'123', 'Name':'111'},

public void PostProName([FromBody]Food value) {}


## 通过客户端调用 WebAPI

修改 Home 控制器中 Index 方法如下：

```cs
public ActionResult Index(){

    //1、创建URI
    Uri uri = new Uri("http://localhost:2222");
    //2、创建一个 HttpClient 客户端对象
    HttpClient httpClient = new HttpClient();
    //3、设置要求 WebAPI 返回的数据类型。默认 json
    httpClient.DefaultRequestHeaders.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));

    //4、设置 HttpClient 客户端获取资源数据的地址
    httpClient.BaseAddress = uri;

    //5、发送一个 get 方法的请求
    var PushAction = httpClient.GetAsync("api/Product");

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


## 路由

MVC 的路由

在 MVC 里面，默认路由机制是通过 url 路径去匹配对应的 action 方法，如 Home/Index 、 Home/GetUser
在 MVC 里面，默认路由位于 APP Start 文件夹下的 RouterConfig.cs 中

在 WebAPI 的默认路由是通过 HTTP 的方法（Get/Post/Put/Delete）去匹配对应的 action，也就是说 webapi 的默认路由不需要指定 action 的名称；
在 WebAPI 里面，默认路由位于 App Start 文件夹下的 WebApiConfig.cs 中

```
config.Routes.MapHttpRoute(
    name: "DefaultApi",
    routeTemplate: "api/{controller}/{id}",
    defaults: new { id = RouteParameter.Optional },
    constraints:new { id=@"\d+"}  //约束
);


config.Routes.MapHttpRoute(
    name: "MyApi",
    routeTemplate: "myapi/{controller}/{action}/{id}",
    defaults: new { id = RouteParameter.Optional }
);
```

特性路由

启用 特性路由

 /* WebApiConfig*/
config.MapHttpAttributeRoutes();

/*Global.asax*/
//WebAPiConfig.Register(GlobalConfiguration.Configuration)
GlobalConfiguration.Configure(WebApiConfig.Register);

使用特性路由
[Route("Values/{id}/GetMyValue")]
public List<Values> Get(){

}


## 跨域 -- 客户端与服务端存在不同的地址或同一地址的不同端口

服务器 webconfig  

system.webserver

节点 

中加一个节点

```xml
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
```


## WebAPI 中的 Session

默认情况下，WebAPI 是无法启用 Session 的

启动 Session 

在 global.asax 中加入

public override void Init()
{
    //注册事件
    this.AuthenticateRequest += WebApiApplication_AuthenticateRequest;
    base.Init();

}
void WebApiApplication_AuthenticateRequst(object sender, EventArgs e)
{

    //启用 webapi 支持 session 会话
    HttpContext.Current.SetSessionStateBehavior(System.Web.SessionState.SessionStateBehavior.Required);
}




//保存
HttpContext.Current.Session["user"] = "F1680502";



## WebAPI 安全解决方案

WebAPI 身份验证


Ajax 请求 beforeSend 在 Headers 中加入 ticket 数据

在 API 中获取该值进行身份验证