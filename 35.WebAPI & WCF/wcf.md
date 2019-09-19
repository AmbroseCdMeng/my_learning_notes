# WCF
## WCF 介绍
### WCF 概念

> WCF（Windows Communication Foundataion：视图通信基础）。
> 
> WCF 是微软推出的一款基于 Windows 平台下开发和部署服务的软件开发包。
> 
> WCF 整合了原有的 Windows 通讯机制（.NET Remoting、WebService、Socket 等），并且融合了 HTTP 和 FTP 等相关技术。是 Windows 平台上分布式开发的最佳实践方式。
>
> 大部分功能都包含在 System.ServiceModel.dll 中

### WCF 作用

- 内外部应用程序接口
- 构建 SOA
- 云平台基础组件

### WCF 特性

- 统一性
    - 完全由托管代码编写
    - WCF 开发与其他 .NET 应用程序开发基本一致，没有什么大的区别

- 互操作性
  - 最基本的通信机制是 SOAP
  - 可以跨进程、跨机器甚至跨平台通信

- 安全可依赖性
  - WS-Security，WS-Trust 和 WS-SecureConversation 均被添加到 SOAP 消息
  - WS-ReliableMessageing 被添加到 SOAP 和 header 中。

- 兼容性
  - 基于 WCF 开发的应用程序，仍然可以直接与 WebService 等应用程序进行交互。


## 使用 Visual Studio 建立 WCF 及调用

### 服务定义

- 契约

    WCF 的基本概念是以契约(Contract) 来定义双方沟通的协议，契约必须要以接口的方式来体现，而实际的服务代码必须要由这些合约接口派生并实现。

    1. 数据契约(DataContract)，标志双方沟通时的数据格式。
    2. 服务契约(ServiceContract)，标志 WCF 服务使用类，定义服务协定。
    3. 操作契约(OperationContract)，标志 WCF 服务具有的方法，定义操作。
    4. 消息契约(MessageContract)，标志在通信期间改写消息内容的规范。

- 宿主

    WCF 服务必须承载在某个进程中，所谓宿主就是控制服务的生存期的应用程序。常用的就是（Windows 服务、WinForm、Console控制台）

### 服务配置

- 终结点 EndPoint
    
    终结点是用来发送或接收消息（或同时发送接收）的构造
- 地址 Address

    在 WCF 框架中，每个服务都具有唯一的地址
- 绑定 Binding

    定义服务器与外部通信方式
- 契约 Contract

    属于一个服务公开的公共接口。声明都可以干什么操作。
---


1. 新建 WCF 服务应用程序

    ![img01](./img/2019-07-22_220246.png) 

2. 编译 WCF 应用程序，然后新建一个控制台程序作为客户端，来调用 WCF 服务

    ![img01](./img/2019-07-22_221555.png)

3. 添加服务引用
   
    ![img01](./img/2019-07-22_221823.png)

4. 输入 WCF 服务地址 http://localhost:63675/Service1.svc 或者点击"发现"可以自动搜索到同一解决方案中的服务
    
    ![img01](./img/2019-07-22_222010.png)

5. 添加 WCF 服务后，在客户端 Program.cs 中调用服务。

    ```csharp
    class Program {
        static void Main(string[] args) {
            Console.WriteLine("wcf test start");
            /* 调用 WCF */
            ServiceReference1.Service1Client sc = new ServiceReference1.Service1Client();
            Console.WriteLine(sc.GetData(100));

            Console.ReadLine();
        }
    }
    ```
    客户端的 app.config 中会自动生成
    ```xml
    <client>
        <endpoint address="http://localhost:63675/Service1.svc" binding="basicHttpBinding"
            bindingConfiguration="BasicHttpBinding_IService1" contract="ServiceReference1.IService1"
            name="BasicHttpBinding_IService1" />
    </client>
    ```

    而 WCF 的 web.config 文件中只有
    ```xml
    <protocolMapping>
        <add binding="basicHttpsBinding" scheme="https" />
    </protocolMapping>    
    ```
    > 这是因为 WCF 集成了 Web 技术，默认使用的 Url 地址是在属性 -- Web 中的 Url

6. 设置解决资源方案启动方式为"多启动"，并设置 WCF 和 客户端的操作为"启动"

    ![img01](./img/2019-07-22_222805.png)

7. 启动项目 

    ![img01](./img/2019-07-22_230448.png)


## 宿主

### 宿主的概念

    宿主就是归属于 Windows 某个进行的应用程序。WCF 服务工作状态受限于宿主的生命周期。宿主与 WCF 服务可以多对多。（宿主相当于一个 Windows 进程，而 WCF 相当于该进程下的线程）


### 宿主的类型

    - 自宿主
      - 控制台
      - Windows 应用程序
      - Windows 服务
    - 其他宿主
      - IIS Express
      - IIS
      - Windows 激活服务

Visual Studio 中新建的 WCF 服务默认的宿主是 IIS Express

![img01](./img/2019-07-22_232027.png)

## 绑定

### 绑定的概念
- 定义了客户端如何与服务进行连接和通信
- 基类为 System.ServiceModel.Channels.Binding
- 绑定的实质是定义信道配置信息

绑定的内容主要包含：传输协议、消息编码、安全性

### 绑定的分类：
- 标准绑定：WCF 框架预先定义的绑定名称。各项参数都有默认值
  - basicHttpBinding
  - wsHttpBinding
  - wsDualHttpBinding
  - wsFederationHttpBinding
  - netNamedPipeBinding
  - netTcpBinding
  - netPeerTcpBinding
  - netMsmqBinding
  - msmqlntergrationBinding
  
- 自定义绑定：基于标准绑定的扩展，根据需要修改配置参数。

## 契约

### 契约的概念
契约是 WCF 框架对外的接口。是实现 WCF 业务逻辑的类的表现形式，根据目的不同具有多种形式表现。

### 契约的类型
- 服务契约（核心契约）
    - 描述客户端能执行的服务操作
    - ServiceContract 用于类上，指示 WCF 此类允许被远程调用
    - OperationContract 用于类中的方法上，指示 WCF 该方法允许被远程调用


- 数据契约
  - 用于自定义数据结构
  - DataContract 用于类上，指示 WCF 此类能够被序列化并传输
  - DataMember 用于类的属性或者字段上，指示 WCF 该属性或字段能够被序列化并传输
- 错误契约
  - 定义访问抛出的错误，以及访问处理错误和传递错误到客户端的方式
  - 关键词 FaultContract， 将错误消息传递给客户端

- 消息契约
  - 用于控制消息格式的消息
  - MessageContract 用于类，指示传递的信息为消息体
  - MessageHeader 用于属性或字段上，指示 WCF 该属性或者阻断传递的消息头消息
  - MessageBody 用于属性或者字段上，指示 WCF 该属性或者字段传递的消息内容

## 客户端调用

## WCF 消息交互模式

## 关联工具

## 配置参数