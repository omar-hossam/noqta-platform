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
  profile_id (random unique number),
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

#### Bill collectors

1. Those people are hired by the government/company and they are responsible to collect bills from users **and add their bill cost to their database so it's saved in their database to use later**
2. They are just for collecting bills nothing else!

- collectors (
  collector_id,
  name,
  gender,
  email,
  phone_number,
  password,
  is_verified, -> verified from the government* **must be true to do actions on users** 
  verified_id,
  city,
  provience,(ميدان العمل)
  issued_bills FOREIGN KEY
)

#### issued_bills

- issued_bills (
  bill_id,
  user_id,
  collector_id,
  month_year, (ex. March 2026)
  bill_cost
)

#### Admins

- Admins can update any data in the app in a very easy way

- admins (
  admin_id,
  username,
  email,
  gender,
  password,
  privilages (read only, read + edit)
)
