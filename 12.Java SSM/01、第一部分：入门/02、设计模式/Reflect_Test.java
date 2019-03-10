

public class Reflect_Test{
    public static void main(String[] args) {
        
    }
}

/* 正常构造类 -- 无参数 */
public class ReflectServiceImpl{
    public static void sayHello(String name) {
        System.err.println("Hello:"+name);
    }
}

/* 反射生成对象 -- 无参数 */
public ReflectServiceImpl getInstance(){
    ReflectServiceImpl object = null;
    try {
        /* 给类加载器注册类 ReflectServiceImpl 的全限定名， 然后通过 newInstance 方法初始化类对象 */
        object = (ReflectServiceImpl)Class.forName("ReflectServiceImpl").newInstance();
    }
    catch (Exception err) {
        System.out.println(err.${getMessage()});
    }
    return object;
}


/* 正常构造类 -- 1 个参数 */
public class ReflectServiceImpl_2 {
    private String name;
    public ReflectServiceImpl_2(String name){
        this.name = name;
    }
    public void sayHello(){
        System.err.println("Hello:"+name);
    }
}

/* 反射构造类 -- 1 个参数 */
public ReflectServiceImpl_2 getInstance(){
    ReflectServiceImpl_2 object = null;
    try {
        /* forName 加载到类加载器 */
        /**
         * forName 加载到类加载器
         * getConstructor 构造方法 -- getConstructor(String.class) 
         *      意为有且只有一个参数类型为 String 的构造方法。通过该方法可以对重名参数排除
         * newInstance 生成对象
         */
        object = (ReflectServiceImpl_2)Class.forName("ReflectServiceImpl_2").getConstructor(String.class).newInstance("ZhangSan");
    }
    catch (Exception err) {
        System.out.println(err.${getMessage()});
    }
    return object;
}


/* 反射方法 */
public Object reflectMethod(){
    Object returnObj = null;
    ReflectServiceImpl target = null;
    try {
        target = (ReflectServiceImpl)Class.forName("ReflectServiceImpl").newInstance();
        /* 第一个参数：方法名称；第二个参数：参数类型，是一个列表，多个参数可以继续编写多个类型 */
        /* 反射方法。第一个参数：调用方法的对象；第二个参数：方法的参数，多个参数可以继续编写。形如：invoke(target, obj1, obj2,……) */
        Method method = ReflectServiceImpl.class.getMethod("SayHello", String.class);
        returnObj = method.invoke(target, "ZhangSan")
    } catch (Exception err) {
        System.out.println(err.${getMessage()});
    }
    return returnObj;
}