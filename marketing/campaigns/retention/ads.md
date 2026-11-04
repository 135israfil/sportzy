# Ads: retargeting and repeat booking (Meta C6, C7)

| Audience | Headline (BN) | Text (BN) | Headline (EN) | Text (EN) | Landing | Event |
|---|---|---|---|---|---|---|
| Visited a venue page, no booking (14 days) | স্লটটা এখনো খালি | যে টার্ফটা দেখছিলে, এই সপ্তাহে ওখানে সন্ধ্যার স্লট খালি আছে। | That slot is still open | The turf you looked at has evening slots open this week. | The same venue page | `booking_completed` |
| Started owner signup, didn't finish | আপনার টার্ফের লিস্টিং প্রায় শেষ | আর ২ মিনিট লাগবে। কোনো সমস্যা হলে WhatsApp করুন। | Your listing is almost done | Two more minutes. WhatsApp us if you're stuck. | Owner signup | `owner_signup_submitted` |
| Viewed a tournament, didn't register | রেজিস্ট্রেশন শুক্রবার বন্ধ | স্পট সীমিত। টিম রেজিস্টার করো, QR Pay BD-তে পে করো। | Registration closes Friday | Limited spots. Register your team and pay by QR Pay BD. | The tournament page | `team_registration_paid` |
| One completed booking 5–25 days ago (C7) | একই সময়, পরের সপ্তাহে? | গত সপ্তাহের মতো এবারও খেলবে? তোমার টার্ফে বৃহস্পতিবার রাত ৯টা খালি। | Same time next week? | Playing again? Your turf has 9 PM free on Thursday. | The venue of their last booking | `booking_completed` (repeat) |

Frequency cap: 2 a week per person. Exclude anyone who booked in the last 3 days.
