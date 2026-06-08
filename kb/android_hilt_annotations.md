
@Inject
声明依赖或声明该类可以被 Dagger 创建。通常和 @Component 或 Hilt 配合使用完成注入。

@Module
定义依赖提供模块，本身不创建对象，需要和 @Provides 或 @Binds 配合使用。

@Provides
定义具体对象的创建逻辑，必须放在 @Module 中使用。常用于 Retrofit、Room、OkHttp 等第三方库。

@Binds
绑定接口与实现类，必须放在 @Module 中使用。用于告诉 Dagger 接口应该使用哪个实现类。

@Component
Dagger 的依赖容器，负责连接 @Inject 和 @Module，将依赖注入到目标对象中。

@Singleton
定义单例作用域，通常需要同时标注在 @Provides、@Inject 类以及 @Component 上才能生效。

@Named
区分多个相同类型的依赖，通常与 @Provides 和 @Inject 配合使用。

@Qualifier
@Named 的增强版，自定义依赖标识，用于大型项目中区分同类型对象。

@HiltAndroidApp
Hilt 应用入口，标注在 Application 上，负责创建应用级依赖容器。

@AndroidEntryPoint
Hilt 注入入口，标注在 Activity、Fragment、Service 等组件上，允许使用 @Inject。

@InstallIn
指定 @Module 安装到哪个 Hilt 容器中，通常与 @Module 配合使用。

@HiltViewModel
让 ViewModel 支持依赖注入，通常与 @Inject 构造函数配合使用。

关系总结：

@Inject + @Component
= 依赖注入

@Module + @Provides
= 提供复杂对象

@Module + @Binds
= 接口绑定实现

@Singleton + @Provides/@Inject
= 单例对象

@Named/@Qualifier + @Inject
= 区分同类型依赖

@HiltAndroidApp + @AndroidEntryPoint
= Hilt 自动注入环境

@Module + @InstallIn
= 将依赖注册到 Hilt 容器

@HiltViewModel + @Inject
= ViewModel 自动注入依赖


# Java 注解（Annotation）总结

## 什么是注解？

Annotation（注解）是一种给代码添加**元数据（Metadata）**的机制。

注解本身不执行任何逻辑，而是提供额外信息给：

- 编译器
- IDE
- 框架
- 代码生成工具

例如：

```java
@Override
public String toString() {
    return "Hello";
}
```

这里的 `@Override` 告诉编译器：

> 当前方法必须重写父类方法。

---

# 为什么需要注解？

## 1. 减少配置

传统 Java：

```xml
<bean id="userService"
      class="com.demo.UserService"/>
```

现代 Spring：

```java
@Service
public class UserService {
}
```

无需 XML。

---

## 2. 配置与代码放在一起

传统方式：

```text
UserService.java
spring.xml
```

需要来回查看。

注解方式：

```java
@Service
public class UserService {
}
```

配置和代码在一起。

---

## 3. 提高开发效率

以前：

```text
创建对象
注册对象
管理生命周期
```

现在：

```java
@Service
```

框架自动完成。

---

# 注解的本质

很多人误以为：

```java
@Service
```

会自动创建对象。

实际上不会。

真正流程：

```text
@Service
    ↓
Spring扫描
    ↓
反射创建对象
    ↓
加入IOC容器
```

所以：

```text
注解 = 标签

框架 = 解释标签的人
```

这是理解注解最重要的一句话。

---

# Java 常见注解

## @Override

检查重写。

```java
@Override
public void run() {

}
```

---

## @Deprecated

标记废弃。

```java
@Deprecated
public void oldMethod() {

}
```

IDE会给出警告。

---

## @SuppressWarnings

忽略警告。

```java
@SuppressWarnings("unchecked")
```

---

# Android 常见注解

## @NonNull

不能为空。

```java
public void save(@NonNull String name) {

}
```

---

## @Nullable

允许为空。

```java
public void save(@Nullable String name) {

}
```

---

## @MainThread

必须运行在主线程。

```java
@MainThread
void updateUI() {

}
```

---

## @WorkerThread

必须运行在后台线程。

```java
@WorkerThread
void loadData() {

}
```

---

# Lombok 注解

Lombok用于减少样板代码。

## 普通写法

```java
public class User {

    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

---

## Lombok写法

```java
@Data
public class User {

    private String name;
}
```

自动生成：

```java
getName()
setName()
toString()
equals()
hashCode()
```

---

# Dagger 2 / Hilt 注解总结

## 什么是 Dagger？

Google官方依赖注入框架。

作用：

```text
管理对象创建
管理对象生命周期
自动依赖注入
```

---

# Dagger 核心注解

## @Inject

告诉Dagger：

> 这个对象可以被自动创建。

### 构造函数注入

```java
public class UserRepository {

    @Inject
    public UserRepository() {

    }
}
```

---

### 字段注入

```java
@Inject
UserRepository repository;
```

---

## @Module

定义依赖提供者。

```java
@Module
public class NetworkModule {

}
```

---

## @Provides

告诉Dagger如何创建对象。

```java
@Module
public class NetworkModule {

    @Provides
    Retrofit provideRetrofit() {
        return new Retrofit.Builder().build();
    }
}
```

---

## @Component

连接所有依赖关系。

```java
@Component(modules = NetworkModule.class)
public interface AppComponent {

    void inject(MainActivity activity);
}
```

关系：

```text
@Module
    ↓
@Component
    ↓
@Inject
```

---

## @Singleton

单例对象。

```java
@Singleton
public class ApiManager {

}
```

整个应用只有一个实例。

---

## @Named

区分同类型对象。

```java
@Provides
@Named("api")
String provideApiUrl() {
    return "https://api.demo.com";
}
```

使用：

```java
@Inject
@Named("api")
String apiUrl;
```

---

## @Qualifier

自定义标识符。

```java
@Qualifier
@Retention(RUNTIME)
public @interface ApiUrl {

}
```

使用：

```java
@Inject
@ApiUrl
String url;
```

大型项目推荐。

---

## @Binds

接口绑定。

```java
@Module
public abstract class RepositoryModule {

    @Binds
    abstract UserRepository bindRepo(
        UserRepositoryImpl impl
    );
}
```

比 @Provides 更高效。

---

## @Scope

自定义生命周期。

```java
@Scope
@Retention(RUNTIME)
public @interface ActivityScope {

}
```

---

# Hilt 常用注解

Hilt = Google官方推荐方案。

本质：

```text
Hilt
    ↓
Dagger2
    ↓
APT/KSP
```

---

## @HiltAndroidApp

Application入口。

```java
@HiltAndroidApp
public class MyApp extends Application {

}
```

---

## @AndroidEntryPoint

Activity/Fragment入口。

```java
@AndroidEntryPoint
public class MainActivity
    extends AppCompatActivity {

}
```

---

## @InstallIn

指定作用域。

```java
@Module
@InstallIn(SingletonComponent.class)
public class NetworkModule {

}
```

---

## @HiltViewModel

ViewModel注入。

```java
@HiltViewModel
public class UserViewModel
    extends ViewModel {

    @Inject
    public UserViewModel(
        UserRepository repo
    ) {

    }
}
```

---

# Dagger 工作流程

```text
@Inject
    ↓
声明需要什么

@Module
    ↓
声明如何创建

@Provides
    ↓
提供对象

@Component
    ↓
建立依赖图

APT/KAPT/KSP
    ↓
生成代码

运行时
    ↓
直接使用生成代码
```

---

# Dagger vs Spring

| 特性 | Spring | Dagger |
|--------|--------|--------|
| 原理 | 反射 | 编译时代码生成 |
| 性能 | 较慢 | 较快 |
| 平台 | 后端 | Android |
| 依赖注入 | IOC | DI |
| 运行时反射 | 大量使用 | 基本不用 |

---

# Android面试必会注解

## Java

```java
@Override
@Deprecated
@SuppressWarnings
```

---

## Android

```java
@NonNull
@Nullable
@MainThread
@WorkerThread
```

---

## Dagger

```java
@Inject
@Module
@Provides
@Component
@Singleton
@Named
@Qualifier
@Binds
@Scope
```

---

## Hilt

```java
@HiltAndroidApp
@AndroidEntryPoint
@InstallIn
@HiltViewModel
```

---

# 一句话总结

现代 Java / Android 开发的核心技术链：

Java
→ Annotation（注解）
→ Reflection（反射）
→ APT/KAPT/KSP（代码生成）
→ Dependency Injection（依赖注入）
→ Framework（Spring / Dagger / Hilt）

理解这条链路，就理解了现代 Java 与 Android 框架的大部分设计思想。