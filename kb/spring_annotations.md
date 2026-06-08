```text
@SpringBootApplication
Spring Boot 启动入口，通常标注在 main 类上。
组合了：
@Configuration + @EnableAutoConfiguration + @ComponentScan

作用：
启动 Spring Boot、开启自动配置、扫描 Bean。

--------------------------------------------------

@Component
通用 Bean 注解。

作用：
把类交给 Spring IOC 容器管理。

@Component
public class UserService {}

--------------------------------------------------

@Service
业务逻辑层 Bean。

本质：
@Component 的语义化版本。

@Service
public class UserService {}

--------------------------------------------------

@Repository
数据访问层 Bean。

本质：
@Component 的语义化版本。

@Repository
public class UserDao {}

--------------------------------------------------

@Controller
MVC 控制器。

作用：
返回页面（JSP、Thymeleaf）。

@Controller
public class UserController {}

--------------------------------------------------

@RestController
REST API 控制器。

本质：
@Controller + @ResponseBody

@RestController
public class UserController {}

返回 JSON：

@GetMapping("/user")
public User getUser() {}

--------------------------------------------------

@Autowired
自动依赖注入。

作用：
从 IOC 容器查找 Bean 并注入。

@Autowired
private UserService service;

--------------------------------------------------

@Resource
Java 标准注入注解。

优先按名称匹配。

@Resource
private UserService service;

面试：
Spring 推荐 Constructor Injection，
@Autowired 逐渐用于构造函数。

--------------------------------------------------

@Configuration
配置类。

作用：
代替 XML 配置文件。

@Configuration
public class AppConfig {}

--------------------------------------------------

@Bean
注册 Bean。

必须放在 @Configuration 中。

@Bean
public ObjectMapper objectMapper() {
    return new ObjectMapper();
}

--------------------------------------------------

@RequestMapping
定义请求路径。

@RequestMapping("/user")

--------------------------------------------------

@GetMapping
GET 请求。

@GetMapping("/list")

--------------------------------------------------

@PostMapping
POST 请求。

@PostMapping("/save")

--------------------------------------------------

@PutMapping
PUT 请求。

@PutMapping("/update")

--------------------------------------------------

@DeleteMapping
DELETE 请求。

@DeleteMapping("/delete")

--------------------------------------------------

@PathVariable
获取 URL 参数。

@GetMapping("/user/{id}")
public User getUser(
    @PathVariable Long id
)

请求：

/user/100

id = 100

--------------------------------------------------

@RequestParam
获取 Query 参数。

@GetMapping("/user")
public User getUser(
    @RequestParam String name
)

请求：

/user?name=leo

--------------------------------------------------

@RequestBody
获取 JSON 请求体。

@PostMapping("/save")
public void save(
    @RequestBody User user
)

--------------------------------------------------

@ResponseBody
返回 JSON。

@ResponseBody
public User getUser(){}

现在一般直接用 @RestController。

--------------------------------------------------

@Value
读取配置文件。

@Value("${server.port}")
private String port;

application.yml

server:
  port: 8080

--------------------------------------------------

@ConfigurationProperties
批量读取配置。

@ConfigurationProperties(prefix="db")
public class DbConfig {}

application.yml

db:
  host: localhost
  port: 3306

--------------------------------------------------

@Transactional
事务管理。

@Transactional
public void saveUser() {

}

作用：

成功：
全部提交

失败：
全部回滚

--------------------------------------------------

@ExceptionHandler
全局异常处理。

@ExceptionHandler(Exception.class)

--------------------------------------------------

@ControllerAdvice
全局 Controller 增强。

通常和 @ExceptionHandler 配合。

@ControllerAdvice
public class GlobalExceptionHandler {}

--------------------------------------------------

@Profile
环境切换。

@Profile("dev")

@Profile("prod")

作用：

开发环境使用不同配置。

--------------------------------------------------

@Scheduled
定时任务。

@Scheduled(
    cron = "0 0 * * * ?"
)

每小时执行一次。

--------------------------------------------------

@Async
异步执行。

@Async
public void sendEmail() {}

需要：

@EnableAsync

--------------------------------------------------

Spring 面试最重要的一组：

启动：
@SpringBootApplication

Bean管理：
@Component
@Service
@Repository
@Configuration
@Bean

依赖注入：
@Autowired
@Resource

Web开发：
@RestController
@RequestMapping
@GetMapping
@PostMapping
@RequestBody
@PathVariable
@RequestParam

事务：
@Transactional

配置：
@Value
@ConfigurationProperties

异步与定时：
@Async
@Scheduled

一句话记忆：

@Component     -> 注册Bean
@Autowired     -> 注入Bean
@Configuration -> 配置Bean
@Bean          -> 创建Bean
@RestController -> 提供API
@Transactional -> 管理事务
@Value         -> 读取配置
@Async         -> 异步执行
@Scheduled     -> 定时任务
```

如果你准备从 Android 转 Java Spring Boot，优先掌握这 15 个注解，基本覆盖 80% 以上的日常开发和面试场景。