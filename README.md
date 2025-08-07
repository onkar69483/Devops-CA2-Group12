# Devops-CA1
Students solutions for their projects submission

🛠️ Fixes & Improvements Overview
✅ Summary
This update resolves the issue where the browser URL was not updating when navigating between different sections and routes of the website. Alongside this, UI improvements for the Contact section and the enhancement of the client logo carousel have been implemented.

These fixes significantly improve navigation, responsiveness, and overall user experience.

🚀 Changes Implemented
1. ✅ Proper Routing Configuration
Replaced outdated or misconfigured routing with BrowserRouter from react-router-dom for clean URL handling.

Ensured all internal links use <Link> for client-side navigation without full page reloads.

Updated route structure to allow real-time URL reflection during navigation.

2. 🔗 Smooth Anchor Navigation
Enabled smooth scrolling for anchor links such as /#contact.

Ensured the browser's address bar updates appropriately even for in-page anchors.

3. 📱 Responsive Contact Section Fixes
Adjusted spacing, font sizes, and flex behavior for improved layout on smaller screens.

Ensured touch-friendly design across common mobile breakpoints.

Fixed alignment issues and maintained consistent design.

4. 🖼️ Client Logo Carousel Upgrade
Replaced the previous logo carousel with a CSS-based continuous marquee.

Features:

Seamless infinite scrolling.

Pauses on hover for better accessibility.

Lighter and more performance-friendly (no external JS libraries required).

🔍 Verified Routes
The following routes have been tested and now update properly in the browser's address bar:

Route	Description
/about	About Us page
/services/kitchen-suppliances	Kitchen Supplies page
/services/qsr-equipments	QSR Equipments page
/services/tabletop-supplies	Tabletop Supplies page
/#contact	Contact section with smooth scroll and proper URL update

🧩 Related Issue
Fixes: #1 – Browser URL not updating during navigation
Fixes: #2 - Clients Section Should Auto Scroll Horizontally and Pause on Hover
Fixes: #3 - Contact Page Input Fields Overflow on Small Screens

👥 Contributors
Username	Contribution
@vasudesai11	Fixed layout issues in the Contact section and replaced the client logo carousel with a CSS marquee.
@harshkharwar1204	Replaced client logo carousel with a CSS-based continuous marquee for better performance and UX.
@dhruvpatel99269	Improved routing structure, verified paths, and ensured browser URL updates for all major navigation flows. Configured BrowserRouter, ensured anchor-based smooth scrolling, and tested client-side navigation thoroughly.