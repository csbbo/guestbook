<template>
  <div class="authregist">
      <div class="panel">
          <span class="title"><router-link to="/login">登录</router-link><router-link to="/regist">注册</router-link></span>
          <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="用户名" prop="username">
                <el-input v-model="ruleForm.username"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="pass">
                <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkPass">
                <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
        </el-form>
      </div>
  </div>
</template>

<script>
import { RegistAPI } from "@/common/api"
export default {
  name: 'AuthRegist',
  data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.ruleForm.checkPass !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.ruleForm.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        ruleForm: {
          username: '',
          pass: '',
          checkPass: '',
        },
        rules: {
          username: [
            { message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            RegistAPI({'username': this.ruleForm.username, 'password': this.ruleForm.pass}).then(resp => {
                if (resp.err != null) {
                    alert(resp.msg);
                } else {
                    this.$router.push({path: '/login'})
                }
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
}
</script>

<style scoped>
    .authregist {
        padding-top: 160px;
    }
    .panel {
        width: 500px;
        margin: auto;
        background-color: #fff;
        padding-top: 40px;
        padding-right: 40px;
        padding-bottom: 20px;
        border-radius: 5px;
    }
    .title {
        font-size: 30px;
        border: 1px solid black;
    }
    a {
        text-decoration: none;
        color: #333333;
        text-align: center;
    }
</style>
