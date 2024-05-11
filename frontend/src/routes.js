/*!

=========================================================
=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import Dashboard from 'views/Dashboard.js';
import {default as Map } from 'views/Map.js';
import TableList from 'views/TableList.js';
import UserProfile from 'views/UserProfile.js';

var routes = [
    {
        path: '/dashboard',
        name: 'Dashboard',
        rtlName: 'لوحة القيادة',
        icon: 'tim-icons icon-chart-pie-36',
        component: <Dashboard />,
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
    // {
    //     path: '/notifications',
    //     name: 'Notifications',
    //     rtlName: 'إخطارات',
    //     icon: 'tim-icons icon-bell-55',
    //     component: <Notifications />,
    //     layout: '/admin',
    // },
    {
        path: '/user-profile',
        name: 'Introduce',
        rtlName: 'ملف تعريفي للمستخدم',
        icon: 'tim-icons icon-single-02',
        component: <UserProfile />,
        layout: '/admin',
    },
    {
        path: '/tables',
        name: 'Library',
        rtlName: 'قائمة الجدول',
        icon: 'tim-icons icon-puzzle-10',
        component: <TableList />,
        layout: '/admin',
    }
];
export default routes;
