# Noqta Platform

That's a simple blueprint of how the system works 

## Who use it?

1. Normal people
2. Organizations
3. Businesses/Shops
4. Admins (developers, gov)
5. Bill collectors MUST-HAVE!

- Each bill collector MUST HAS AN ACCOUNT ON THE PLATFORM CORRESPONDED WITH HIS INFO FROM THE OFFICIAL SOURCES FROM THE GOVERNMENT AND FROM WATER COMPANY 

## Categories

- Houses, Apartments = المنازل والشقق (السكني)
- Religious places = دور العبادة
- Government places = الجهات الحكومية
- Commercial = النشاط التجاري 
  - stores
  - restaurants
  - cafes
  - barbers
  - ...
- Industries = النشاط الصناعي
- Hotels / Tourism villages = الفنادق والقرى السياحية
- Clubs = الأندية الرياضية
- gas stations = محطات الوقود
- Service/Charity = الجمعيات الخيرية والخدمية 

## Database

### Tables

#### Users

What are the user's activities?

1. he can complete daily water saving checks **streak += 1**
  - that will increase **XP+**
2. Why **City?** so he could be **monthly_ranked**
3. he has **friends** each **friend** is a *user*
4. each user has badges shown on his profile 
5. **Bill collector** is responsible to **increase or decrease user's XP depending on water usage**
6. user can send & receive friend requests

- users (
  user_id, 
  name, 
  gender,
  city, 
  street,
  password,
  email,
  phone_number,
  building_type, 
  xp, 
  joined_date,
  badges,
  streak,
  monthly_rank, 
  friends,
  monthly_bills,
  friend_requests_get,
  friend_requests_send
)
