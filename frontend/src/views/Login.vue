<template>
  <div class="login-box">
    <h2>登录</h2>

    用户名<input type="text" v-model="username">
    <br><br>
    密码 <input type="password" v-model="password">
    <br><br>
    <button @click="login">登录</button>
    <p>{{message}}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data(){
    return{
      username: "",
      password: "",
      message:  "",
    };
  },

  methods:{
    async login(){
      try{
        const res = await axios.post(
            "http://127.0.0.1:5000/api/user/login",
            {
              username: this.username,
              password: this.password
            }
        );
        this.message = res.data.message;
      }catch(err){
        this.message = "请求失败"
      }
    }
  }
}

</script>

<style>
.login-box{
  width: 300px;
  margin: 100px auto;
  text-align: center;
}
</style>