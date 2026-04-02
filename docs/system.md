# Noqta Platform

That's a simple blueprint of how the system works 

## Who use it?

1. Normal people
2. Bill collectors MUST-HAVE!
3. Admins (developers, gov)

- Each bill collector MUST HAS AN ACCOUNT ON THE PLATFORM CORRESPONDED WITH HIS INFO FROM THE OFFICIAL SOURCES FROM THE GOVERNMENT AND FROM WATER COMPANY 

## Pages

### Logged Out

1. / 
2. /login -> contains both user and collector 
3. /register -> creates new user account
4. /admin -> for admin

any other page will redirect to login for security

### Logged in

- /leaderboard -> shows leaderboard
- /profile 
- /friends
- /preferences 
- /dashboard 

### Shows only once 

- AFTER /register DONE SHOW /building-type

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
  xp, 
  joined_date,
  streak,
  monthly_rank, 
  friends,
  monthly_bills,
  friend_requests_get,
  friend_requests_send,
  
  // social 
  bio,
  facebook_link,
  whatsapp_number
)

#### Monthly Leaderboard

1. Monthly leaderboard ranks people in each city or the entire country and motivates them with prizes, coupons and redems

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
  code,
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
