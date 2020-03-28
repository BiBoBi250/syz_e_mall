import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'     //导入登录组件
import Register from '@/components/Register'  //导入注册组件


Vue.use(Router)


export default new Router({
  routes: [
    {           //登录界面
      path: '/',
      name: 'Login',
      component: Login
    },
    {            //导入注册页面
      path:'/',
      name:'Register',
      component: Register
    }
  ]

})

