const isDarkTheme = window.matchMedia("(prefers-color-scheme: dark)");
const main_html = document.getElementById("html");

class ThemeManager {
    // 管理主题变化，并支持增加回调函数来处理诸如 vditor 的主题跟随网站切换
    private funcs: ((theme: "light" | "dark") => void)[] = [];

    constructor() {}

    public addCallback(func: ((theme: "light" | "dark") => void)): void {
        // 增加切换主题时执行的额外回调
        // 增加的函数需要传入以下参数：theme: "light" | "dark"
        this.funcs.push(func);
    }

    private runCallback(theme: "light" | "dark") {
        for (const func of this.funcs) {
            func(theme);
        }
    }

    private changeThemeToSystem () {
        // 根据系统或浏览器设置切换主题
        if (isDarkTheme.matches) {
            main_html.setAttribute("class", "dark");
            this.runCallback("dark");
            console.log("跟随系统设置，切换网站为深色模式。")
        }
        else {
            main_html.setAttribute("class", "light");
            this.runCallback("light");
            console.log("跟随系统设置，切换网站为浅色模式。")
        }
    }

    public changeThemeByUser () {
        // 主动切换主题（用户点击切换按钮），并保存 cookie
        // 切换主题之后，将主题保存在 cookie 中
        let theme = main_html.getAttribute("class");
        if (theme === "dark") {
            main_html.setAttribute("class", "light");
            document.cookie = "theme=light; path=/";
            this.runCallback("light");
            console.log("主动切换网站为浅色模式。")
        }
        else {
            main_html.setAttribute("class", "dark");
            document.cookie = "theme=dark; path=/";
            this.runCallback("dark");
            console.log("主动切换网站为深色模式。")
        }
    }

    public loadTheme () {
        // 在页面加载时调用此函数以加载主题，如果有 cookie 会自动处理。
        console.log("开始加载主题...")
        let themeSet = false;
        document.cookie.split(";").forEach((cookie) => {
            if (cookie.indexOf("theme=") >= 0) {
                themeSet = true;
                let theme = cookie.replace(" theme=", "").replace("theme=", "")
                console.log("读取保存的主题设置 cookie：" + theme)
                if (theme == "dark") {
                    main_html.setAttribute("class", "dark");
                    this.runCallback("dark");
                } else {
                    main_html.setAttribute("class", "light");
                    this.runCallback("light");
                }
            }
        })
        if (!themeSet) {
            this.changeThemeToSystem();
        }
    }
}
