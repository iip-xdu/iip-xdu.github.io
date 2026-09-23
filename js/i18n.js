/* ==========================================================================
   IIP Lab website - lightweight bilingual switcher (EN <-> 中文)
   - Default language: English
   - Click the language icon in the top-right navbar to switch
   - Choice is remembered in localStorage
   - Long blocks are translated through the data-zh attribute,
     short strings through the DICT table below.
   ========================================================================== */
(function () {
    'use strict';

    var STORE_KEY = 'iip-lang';
    var DEFAULT_LANG = 'en';

    /* ----------------------------------------------------------------------
       Short strings: English -> Chinese
       ---------------------------------------------------------------------- */
    var DICT = {
        /* --- navigation / common --- */
        "Home": "首页",
        "Team": "团队成员",
        "Research": "研究方向",
        "About Us": "关于我们",
        "Team Members": "团队成员",
        "Research Topics": "研究方向",
        "Contact": "联系方式",
        "Links": "相关链接",
        "Pages": "页面导航",
        "Laboratory": "实验室",
        "Join Us": "加入我们",
        "Loading...": "加载中...",
        "Newsletter": "订阅",

        /* --- home --- */
        "Welcome to IIP Lab.": "欢迎来到智能信息处理（IIP）实验室",
        "Intelligent Information Processing (IIP) Lab.": "智能信息处理（IIP）实验室",
        "Xidian University": "西安电子科技大学",
        "Recent News": "近期动态",
        "Publications": "学术论文",
        "Students": "学生",
        "Phd/Master": "博士/硕士",
        "Top/CCF-A": "Top/CCF-A",

        /* --- research --- */
        "Research Projects": "研究方向",
        "Embodied Intelligence": "具身智能",
        "Visual Understanding": "视觉理解",
        "Artificial Intelligence Generated Content (AIGC)": "人工智能生成内容（AIGC）",
        "full list on DBLP": "DBLP 完整列表",

        /* --- team --- */
        "Academic Staffs": "教师队伍",
        "Ph.D. Candidates": "在读博士生",
        "Master Students": "在读硕士生",
        "Ph.D. Students": "博士生",
        "Postgraduates": "指导学生",
        "Alumni": "往届学生",
        "Alumni · PH.D.": "博士毕业生",
        "Alumni · Postgraduates": "硕士毕业生",

        /* --- member pages --- */
        "About Me": "个人简介",
        "Selected Publications": "代表性论文",

        /* --- academic titles --- */
        "Professor": "教授",
        "Associate Professor": "副教授",
        "Assistant Professor": "助理教授",
        "Lecturer": "讲师",
        "Distinguished Professor": "特聘教授",

        /* --- contact / footer --- */
        "No. 2 South Taibai Road,": "西安市太白南路 2 号",
        "Xi’an, Shaanxi 710071, China": "中国 · 陕西 · 西安 710071",

        /* --- faculty --- */
        "Nannan Wang": "王楠楠",
        "Fei Gao": "高飞",
        "Chunlei Peng": "彭春蕾",
        "De Cheng": "程德",
        "Mingrui Zhu": "朱明瑞",
        "Jingwei Xin": "辛经纬",
        "Decheng Liu": "刘德成",
        "Hangyu Li": "李航宇",
        "Xinpeng Ding": "丁鑫棚",

        /* --- destinations: Ph.D. alumni --- */
        "2016, Xiamen Univ. (Prof., National Young Talent)": "2016，厦大（教授，国家级青年人才）",
        "2017, XDU (Prof., National Young Talent)": "2017，西电（教授，国家级青年人才）",
        "2017, XDU": "2017，西电",
        "2019, Xuzhou Institute of Technology": "2019，徐州工程学院",
        "2020, XDU (ISN)": "2020，西电 ISN 全国重点实验室",
        "2020, Tianjin Univ. (Prof.)": "2020，天大（教授）",
        "2020, XDU (School of Computer Science)": "2020，西电计算机学院",
        "2021, Huawei": "2021，华为",
        "2021, XDU (ISN)": "2021，西电 ISN 全国重点实验室",
        "2021, XDU": "2021，西电",
        "2023, HKBU (Postdoc); XDU": "2023，浸会大学（博士后）；西电",
        "2023, HKUST (Postdoc); Tianjin Univ. (Assoc. Prof.)": "2023，港科大（博士后）；天大（副教授）",
        "2024, Beijing Normal Univ. (Postdoc)": "2024，北师大（博士后）",
        "2024, City Univ. of Macau (Asst. Prof.)": "2024，澳门城大（助理教授）",
        "2025, Hefei Univ. of Tech. (Lecturer)": "2025，合工大（讲师）",
        "2025, Alibaba Tongyi Wanxiang (A-Star)": "2025，阿里通义万相（A-Star）",
        "2026, CQUPT (Assoc. Prof.)": "2026，重邮（副教授）",
        "2026, Kuaishou Kling (Kua-Star)": "2026，快手可灵（快-Star）",

        /* --- destinations: master alumni --- */
        "2012, Baidu": "2012，百度",
        "2013, CETC Institute 54": "2013，中电 54 所",
        "2014, 360 Corporation": "2014，360 公司",
        "2017, CETC Institute of Intelligence": "2017，中电科智能院",
        "2017, Hikvision": "2017，海康威视",
        "2018, CETC Institute 38": "2018，中电 38 所",
        "2021, HKUST (PhD); XDU": "2021，港科大读博；西电",
        "2022, CETC Institute 54": "2022，中电 54 所",
        "2022, ZTE": "2022，中兴",
        "2022, Longhu Digital Tech.": "2022，龙湖数科",
        "2023, Horizon Robotics": "2023，地平线",
        "2023, XDU (PhD study)": "2023，硕博连读",
        "2023, Hengxuan Tech. (Shanghai)": "2023，上海恒玄科技",
        "2023, Huzhou No.2 High School (Zhejiang)": "2023，浙江湖州二中",
        "2024, Agricultural Bank of China (Fujian Branch)": "2024，农行福建分行",
        "2024, Xi'an Zhaoxin IC": "2024，西安兆芯",
        "2024, Zhaoxin Semiconductor (Xi'an)": "2024，西安兆芯",
        "2024, Mindray Medical": "2024，迈瑞医疗",
        "2024, iFlytek": "2024，科大讯飞",
        "2025, ByteDance": "2025，字节跳动",
        "2025, Alibaba": "2025，阿里",
        "2025, Meituan": "2025，美团",
        "2025, NetEase Games": "2025，网易游戏",
        "2025, Ant Group": "2025，蚂蚁集团",
        "2025, Vivo": "2025，VIVO",
        "2025, JD.com": "2025，京东",
        "2026, Pony.ai": "2026，小马智行",
        "2026, HKUST (PhD study)": "2026，港科大读博",
        "2026, Tencent": "2026，腾讯",
        "2026, XDU (Research Assistant / PhD study)": "2026，西电科研助理，读博",
        "2026, Baidu": "2026，百度",

        /* --- document titles --- */
        "IIP Lab.": "IIP 实验室",
        "IIP · Research": "IIP · 研究方向",
        "IIP · Team": "IIP · 团队成员",
        "IIP · Nannan Wang": "IIP · 王楠楠",
        "IIP · Fei Gao": "IIP · 高飞",
        "IIP · Chunlei Peng": "IIP · 彭春蕾",
        "IIP · De Cheng": "IIP · 程德",
        "IIP · Mingrui Zhu": "IIP · 朱明瑞",
        "IIP · Jingwei Xin": "IIP · 辛经纬",
        "IIP · Decheng Liu": "IIP · 刘德成",
        "IIP · Hangyu Li": "IIP · 李航宇",
        "IIP · Xinpeng Ding": "IIP · 丁鑫棚",

        /* --- faculty (missing) --- */
        "Xin Wei": "卫鑫",
        "Xinbo Gao": "高新波",
        "Bo Han": "韩波",
        "Xianye Ben": "贲晛烨",
        "Jian Sun": "孙剑",

        /* --- academic titles --- */
        "Director, Distinguished Professor": "主任，特聘教授",
        "Xianghu Elite Professor": "湘湖菁英教授",
        "Assistant Researcher, Xianghu Elite Professor": "副研究员，湘湖菁英教授",
        "Huashan Associate Professor": "华山学者副教授",
        "2026.02 - Present: Professor, Hangzhou Institute of Technology, Xidian University": "2026.02 - 至今：教授，西安电子科技大学杭州研究院",
        "2025.08 - 2026.01: Postdoctoral Researcher, HKUST": "2025.08 - 2026.01：博士后研究员，香港科技大学",
        "2024.05 - 2025.05: Research Intern, Huawei Noah's Ark Lab, Hong Kong": "2024.05 - 2025.05：研究实习生，华为诺亚方舟实验室（香港）",
        "2021.09 - 2025.07: Ph.D. in Electronic and Computer Engineering, HKUST (Advisor: Prof. Xiaomeng Li)": "2021.09 - 2025.07：电子与计算机工程专业博士，香港科技大学（导师：Prof. Xiaomeng Li）",
        "2020.07 - 2021.07: Research Intern, Alibaba DAMO Academy, Hangzhou": "2020.07 - 2021.07：研究实习生，阿里巴巴达摩院（杭州）",
        "2018.09 - 2021.07: M.S. in Information and Communication Engineering, Xidian University (Advisors: Prof. Xinbo Gao, Prof. Nannan Wang)": "2018.09 - 2021.07：信息与通信工程专业硕士，西安电子科技大学（导师：高新波 教授、王楠楠 教授）",
        "2014.08 - 2018.07: B.S. in Software Engineering, Xidian University": "2014.08 - 2018.07：软件工程专业学士，西安电子科技大学",
        "Huashan Elite Associate Professor": "华山学者菁英副教授",
        "Huashan Tenure-track Associate Professor": "华山学者准聘副教授",
        "Huashan Assistant Professor": "华山学者助理教授",
        "Post-doctoral Research Fellow": "博士后研究员",
        "Research Intern": "研究实习生",
        "First/Corresponding": "第一/通讯作者",
        "Journal/Conference": "期刊/会议",

        /* --- section headings --- */
        "Our Team": "我们的团队",
        "Education & Work Experience": "教育经历与工作经历",
        "Education & Experience": "教育经历与工作经历",
        "Education": "教育经历",
        "Experience": "工作经历",
        "Service": "学术服务",
        "Academic Service": "学术服务",
        "Master's Students": "硕士研究生",
        "Area Chair": "领域主席",
        "Guest Editor": "客座编辑",
        "Associate Editor": "副编辑",
        "Conference Reviewer": "会议审稿人",
        "Journal Reviewer": "期刊审稿人",
        "2025.07 - Present": "2025.07 - 至今",

        /* --- education / institution strings --- */
        "B.Eng. in Electronic and Information Engineering": "电子信息工程专业（工学学士）",
        "Ph.D. in Information and Telecommunications Engineering": "信息与通信工程专业（工学博士）",
        "Shandong University (Advisor: Prof. Xianye Ben)": "山东大学（导师：贲晛烨 教授）",
        "Xidian University (Advisor: Prof. Nannan Wang)": "西安电子科技大学（导师：王楠楠 教授）",
        "Department of Computer Science, Hong Kong Baptist University (Advisor: Dr. Bo Han)": "香港浸会大学计算机科学系（导师：韩波 教授）",
        "Tencent AI Lab (Advisor: Dr. Zhifeng Li)": "腾讯 AI Lab（导师：李志峰 博士）",
        "Shenzhen Intellifusion Technologies Co. Ltd. (Advisor: Dr. Xiaoyu Wang, IEEE Fellow)": "深圳云天励飞技术股份有限公司（导师：王孝宇 博士，IEEE Fellow）",
        "National Key Laboratory of Space-Ground Integrated Information Technology, Xidian University": "西安电子科技大学空天地一体化综合业务网全国重点实验室",
        "State Key Laboratory of Integrated Services Networks, Xidian University": "西安电子科技大学综合业务网理论及关键技术国家重点实验室",
        "ICASSP, IJCNN": "ICASSP、IJCNN",
        "Machine Learning (Springer), Symmetry (MDPI)": "Machine Learning（Springer）、Symmetry（MDPI）",
        "IEEE TPAMI, IEEE TIP, IEEE TNNLS, Scientific Reports": "IEEE TPAMI、IEEE TIP、IEEE TNNLS、Scientific Reports",
        "CVPR, ICCV, NeurIPS, ICML, ICLR": "CVPR、ICCV、NeurIPS、ICML、ICLR",
        "Selected publications in CCF-A conferences and top journals (IEEE Transactions, IJCV) over the last three years (2024–2026). See the": "近三年（2024–2026）发表于 CCF-A 类会议与顶级期刊（IEEE Transactions、IJCV）的代表性论文。详见",

        /* --- footer --- */
        "Hangzhou Institute": "西电杭州研究院",
        "ISN State Key Lab.": "ISN 国家重点实验室",
        "VIPSL (Xinbo Gao)": "VIPSL（高新波）",
        "Designed By": "设计：",
        ", All Right Reserved.": "，版权所有。",
        ", All Right Reserved. Designed By": "，版权所有。设计：",
        "Cookies": "Cookie 政策",
        "Help": "帮助",
        "FQAs": "常见问题",
        "[DBLP]": "【DBLP】",
        "[Google Scholar]": "【Google Scholar】",
        "[GitHub]": "【GitHub】",
        "[Homepage]": "【个人主页】",
        "[Personal Web]": "【个人主页】",
        "Xi'an, Shaanxi 710071, China": "中国 · 陕西 · 西安 710071"
    };

    /* ----------------------------------------------------------------------
       Sub-string replacements (applied to Chinese mode only).
       Used for names / organizations that appear INSIDE longer sentences,
       where a whole-string dictionary match is not possible.
       Order matters: longer patterns first.
       ---------------------------------------------------------------------- */
    var SUBS = [
        /* people */
        [/Nannan Wang/g, "王楠楠"],
        [/Xinbo Gao/g, "高新波"],
        [/Xinpeng Ding/g, "丁鑫棚"],
        [/Chunlei Peng/g, "彭春蕾"],
        [/Mingrui Zhu/g, "朱明瑞"],
        [/Jingwei Xin/g, "辛经纬"],
        [/Decheng Liu/g, "刘德成"],
        [/Hangyu Li/g, "李航宇"],
        [/Xin Wei/g, "卫鑫"],
        [/Bo Han/g, "韩波"],
        [/Xianye Ben/g, "贲晛烨"],
        [/Jian Sun/g, "孙剑"],
        [/Zhifeng Li/g, "李志峰"],
        [/Xiaoyu Wang/g, "王孝宇"],

        /* organizations / venues */
        [/\bAlibaba Tongyi Wanxiang\b/g, "阿里通义万相"],
        [/\bKuaishou Kling\b/g, "快手可灵"],
        [/\bAnt Group\b/g, "蚂蚁集团"],
        [/\bByteDance\b/g, "字节跳动"],
        [/\bNetEase Games\b/g, "网易游戏"],
        [/\bPony\.ai\b/g, "小马智行"],
        [/\bMeituan\b/g, "美团"],
        [/\biFlytek\b/g, "科大讯飞"],
        [/\bHorizon Robotics\b/g, "地平线"],
        [/\bMindray Medical\b/g, "迈瑞医疗"],
        [/\bHikvision\b/g, "海康威视"],
        [/\bHuawei\b/g, "华为"],
        [/\bBaidu\b/g, "百度"],
        [/\bTencent\b/g, "腾讯"],
        [/\bAlibaba\b/g, "阿里"],
        [/\bJD\.com\b/g, "京东"],
        [/\b360 Corporation\b/g, "360 公司"],
        [/\bHengxuan Tech\. \(Shanghai\)/g, "上海恒玄科技"],
        [/\bCETC Institute of Intelligence\b/g, "中电科智能院"],
        [/\bCETC Institute 54\b/g, "中电科技集团第 54 研究所"],
        [/\bCETC Institute 38\b/g, "中电 38 所"],
        [/\bLonghu Digital Tech\.\b/g, "龙湖数科"],
        [/\bAgricultural Bank of China \(Fujian Branch\)/g, "农行福建分行"],
        [/\bZhaoxin Semiconductor \(Xi'an\)/g, "西安兆芯"],
        [/\bXi'an Zhaoxin IC\b/g, "西安兆芯"],
        [/\bBeijing Normal Univ\.\b/g, "北师大"],
        [/\bHefei Univ\. of Tech\.\b/g, "合工大"],
        [/\bCity Univ\. of Macau\b/g, "澳门城大"],
        [/\bXiamen Univ\.\b/g, "厦大"],
        [/\bCQUPT\b/g, "重邮"],
        [/\bHKUST\b/g, "港科大"],
        [/\bHKBU\b/g, "浸会大学"],
        [/\bXDU\b/g, "西电"],
        [/\bXidian University\b/g, "西电"],
        [/\bTianjin Univ\.\b/g, "天大"],
        [/\bZTE\b/g, "中兴"]
    ];

    /* ----------------------------------------------------------------------
       Engine
       ---------------------------------------------------------------------- */
    var originals = new WeakMap();

    function norm(s) {
        return (s || '').replace(/\s+/g, ' ').trim();
    }

    var SKIP_TAGS = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEMPLATE: 1, TEXTAREA: 1 };

    function inZhBlock(node) {
        var el = node.parentElement;
        while (el) {
            if (el.tagName && SKIP_TAGS[el.tagName]) return true;
            if (el.hasAttribute && el.hasAttribute('data-zh')) return true;
            el = el.parentElement;
        }
        return false;
    }

    function inKeepEn(node) {
        var el = node.parentElement;
        while (el) {
            if (el.hasAttribute && el.hasAttribute('data-keep-en')) return true;
            el = el.parentElement;
        }
        return false;
    }

    function subAll(str) {
        var out = str;
        for (var i = 0; i < SUBS.length; i++) {
            out = out.replace(SUBS[i][0], SUBS[i][1]);
        }
        // alumni / year entries: "2026, Baidu" -> "2026，百度"
        if (/^\d{4},\s/.test(out)) out = out.replace(', ', '，');
        return out;
    }

    function applyBlocks(lang) {
        var blocks = document.querySelectorAll('[data-zh]');
        for (var i = 0; i < blocks.length; i++) {
            var el = blocks[i];
            if (!el.__enHtml) el.__enHtml = el.innerHTML;
            el.innerHTML = (lang === 'zh') ? el.getAttribute('data-zh') : el.__enHtml;
        }
    }

    function applyText(lang) {
        var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        var nodes = [];
        while (walker.nextNode()) nodes.push(walker.currentNode);
        for (var i = 0; i < nodes.length; i++) {
            var n = nodes[i];
            if (!n.parentElement || inZhBlock(n) || inKeepEn(n)) continue;
            if (!originals.has(n)) originals.set(n, n.nodeValue);
            var base = originals.get(n);
            if (lang === 'zh') {
                var key = norm(base);
                n.nodeValue = DICT[key] ? DICT[key] : subAll(base);
            } else {
                n.nodeValue = base;
            }
        }
    }

    function applyTitle(lang) {
        if (!originals.has(document)) originals.set(document, document.title);
        var base = originals.get(document);
        var key = norm(base);
        document.title = (lang === 'zh' && DICT[key]) ? DICT[key] : base;
    }

    function applyMeta(lang) {
        var html = document.documentElement;
        html.setAttribute('lang', lang === 'zh' ? 'zh-CN' : 'en');
        var toggles = document.querySelectorAll('.lang-toggle');
        for (var i = 0; i < toggles.length; i++) {
            var t = toggles[i];
            t.setAttribute('title', lang === 'zh' ? 'Switch to English' : '切换为中文');
            t.setAttribute('aria-label', lang === 'zh' ? 'Switch to English' : '切换为中文');
            var label = t.querySelector('.lang-label');
            if (label) label.textContent = lang === 'zh' ? 'EN' : '中文';
        }
    }

    function current() {
        try {
            return localStorage.getItem(STORE_KEY) || DEFAULT_LANG;
        } catch (e) {
            return DEFAULT_LANG;
        }
    }

    function apply(lang) {
        applyBlocks(lang);
        applyText(lang);
        applyTitle(lang);
        applyMeta(lang);
        try { localStorage.setItem(STORE_KEY, lang); } catch (e) {}
    }

    function toggle() {
        apply(current() === 'zh' ? 'en' : 'zh');
    }

    function bind() {
        var toggles = document.querySelectorAll('.lang-toggle');
        for (var i = 0; i < toggles.length; i++) {
            (function (el) {
                if (el.getAttribute('href') === '' || el.getAttribute('href') === '#') {
                    el.setAttribute('href', 'javascript:void(0)');
                }
                el.addEventListener('click', function (e) {
                    e.preventDefault();
                    toggle();
                });
            })(toggles[i]);
        }
    }

    function init() {
        bind();
        apply(current());
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
