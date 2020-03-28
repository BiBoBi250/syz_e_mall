<template>
  <div class="register_form">
    <section class="form_container">
      <el-form :model="registerUser" :rules="rules" class="registerForm" ref="registerForm" label-width="80px">
        <el-form-item label="用户名" prop="name">
          <el-input v-model="registerUser.name" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerUser.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerUser.password" placeholder="请输入密码" type="password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="password2">
          <el-input v-model="registerUser.password2" placeholder="请确认密码" type="password"></el-input>
        </el-form-item>
        <el-form-item label="选择身份">
          <el-select v-model="registerUser.identity" placeholder="请选择身份">
            <el-option label="商家" value="shopKeeper"></el-option>
            <el-option label="用户" value="normalUser"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary"  class="submit_btn" @click="submitForm('registerForm')">注 册</el-button>
        </el-form-item>
      </el-form>
    </section>
  </div>
</template>

<script>
  export default {
    name: "Register",
    data() {
      var validatePass2 = (rule, value, callback) => {
        if (value !== this.registerUser.password) {
          callback(new Error("两次输入密码不一致"));
        } else {
          callback();
        }   //密码与确认密码不相同时提示两次输密码不一致
      };
      return {
        registerUser: {
          name: "",          //用户名
          email: "",         //邮箱号
          password: "",      //密码
          password2: "",     //确认密码
          identity: ""
        },
        //简单验证表单信息
        name: [              //用户名不为空且长度在2-20字符
          {required: ture, message: "用户名不能为空", trigger: "change"},
          {min: 2, max: 20, message: "长度在2到20字符", trigger: "blur"}
        ],
        email: [             //验证邮箱格式
          {type: "email", required: true, message: "邮箱格式不正确", trigger: "blur"}
        ],
        password: [          //密码不为空且长度在6-20字符
          {required: true, message: "密码不能为空", trigger: "blur"},
          {min: 6, max: 20, message: "长度在6到20字符", trigger: "blur"}
        ],
        password2: [         //密码不为空且上一次密码相同
          {required: true, message: "密码不能为空", trigger: "blur"},
          {min: 6, max: 20, message: "长度在6到20字符", trigger: "blur"},
          {validator: validatePass2, trigger: "blur"}
        ]
      }
    },
    methods: {               //实现submit_btn的submitForm('registerForm')方法
        submitForm(formName){
          /*this.$refs[formName].validate(valid=>{
            if (valid) {
              this.$axios
                .post("/api/users/register", this.registerUser)
                .then(res => {
                  // 注册成功
                  this.$message({
                    message: "注册成功！",
                    type: "success"
                  });
                   //this.$router.push("/Login");
                });
            } else {
              console.log("error submit!!");
              return false;
            }*/
          this.$router.push("/Login");
        }
    }
  }
</script>

<style scoped>

</style>
