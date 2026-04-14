# چشم‌انداز OTP در Notification Framework (نسخه خلاصه)

## نسخه ۱ — وضعیت فعلی
OTP در نسخهٔ اول یک Feature ساده، پایدار و قابل استفاده است که شامل:
- service (تولید و مدیریت کد)
- message (ساخت پیام)
- view (ارائه endpoint آماده)

در این نسخه هدف «سادگی و کاربردی بودن» است، نه معماری قابل برنامه‌ریزی.

## چرا ساده؟
معماری برنامه‌پذیر OTP نیازمند بخش‌های پیشرفته‌تری است:
- template قابل override
- code generator قابل تزریق
- context و policyهای امنیتی
- انتخاب کانال‌ها
- mapper و formatter
- multi-channel / multi-step flows

ورود این موارد در نسخه ۱ باعث پیچیدگی غیرضروری می‌شود.  
بنابراین OTP نسخه ۱ عامدانه ساده نگه داشته شده است.

## تمرکز فعلی فریمورک
قبل از پیچیده کردن Featureها، باید زیرساخت اصلی کامل شود:
- Dispatching
- مدیریت کانال‌ها
- Canonical Message
- ارسال Pipeline

OTP نسخه ۱ همین حالا قابل استفاده است و تا تکمیل هسته، تغییر بنیادی نمی‌کند.

## نسخه‌های آینده (+2)
OTP تبدیل خواهد شد به یک Feature برنامه‌پذیر:
- جریان‌های قابل تعریف (login, reset password, device verify, …)
- Template / Mapper / Generator قابل تزریق
- Context و policyهای امنیتی
- Channel resolver قابل پیکربندی

OTP در آینده پایهٔ معماری سایر Featureهای برنامه‌پذیر (Reset Password, Login Alert, etc) خواهد شد.
