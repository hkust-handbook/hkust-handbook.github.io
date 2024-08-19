# Courses

Choose subjects on the left.

部分爬取自微信号“HKUST课堂笔记集散地”。

# Enrollment

1. How to use the Timetable Planner in advance:
    - Chrome extension: [https://chromewebstore.google.com/detail/hkust-timetable-addon/amgobcacdjcliphhejphfhcdhaikhcme](https://chromewebstore.google.com/detail/hkust-timetable-addon/amgobcacdjcliphhejphfhcdhaikhcme)
    - Open the browser Console and type `$("#semester").val("yyss");`, where `yy` is the academic year (e.g., `24` for 2024-25 academic year) and `ss` is the semester code (`10`, `20`, `30`, and `40`, for fall, winter, spring, and summer, resp.) Complete example: `$("#semester").val("2410");`.
2. You cannot add a class that has a time conflict with a class in which you are
   already successfully enrolled. However, you are allowed to do so if the class
   only conflicts with a class for which you are on the waitlist. It is
   important to note that this may lead to undesired outcomes.

    For example,
    let's say you prefer course A over B, but they have a scheduling
    conflict. You added yourself to the waitlist for course A first and later
    successfully enrolled in course B. However, enrolling in course B prevents
    you from enrolling in course A. Additionally, there is a possibility that
    other students on the waitlist may secure a spot ahead of you.
