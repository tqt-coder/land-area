/*!

=========================================================
=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import Dashboard from 'views/Dashboard.js';
import {default as Map } from 'views/Map.js';
// import TableList from 'views/TableList.js';
import UserProfile from 'views/UserProfile.js';
import Logout from 'views/logout';
import NewsPage from 'views/NewsPage';
var routes = [
    {
        path: '/user-profile',
        name: 'Introduce',
        rtlName: 'ملف تعريفي للمستخدم',
        icon: 'tim-icons icon-single-02',
        component: <UserProfile />,
        layout: '/admin',
    },
    {
        path: '/map',
        name: 'Map',
        rtlName: 'خرائط',
        icon: 'tim-icons icon-pin',
        component: <Map />,
        layout: '/admin',
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        rtlName: 'لوحة القيادة',
        icon: 'tim-icons icon-chart-pie-36',
        component: <Dashboard />,
        layout: '/admin',
    },
    {
        path: '/logout',
        name: 'Logout',
        rtlName: 'إخطارات',
        icon: 'tim-icons icon-button-power',
        component: <Logout />,
        layout: '/admin',
    },
    {
        path: '/new-page',
        name: 'News',
        rtlName: 'قائمة الجدول',
        icon: 'tim-icons icon-bell-55',
        component: <NewsPage />,
        layout: '/admin',
    },
];
export default routes;
