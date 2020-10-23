<template>
  <div class="width">
    <el-row>
      <el-col :span="24">
        <div class="input">
          <el-input placeholder="input your to do list" v-model="inputValue">
            <el-button slot="append" icon="el-icon-check" @click="addItemList" style="font-size: 20px"></el-button>
          </el-input>
        </div>
      </el-col>
    </el-row>
    <el-row class="items">
      <el-col :span="24">
        <el-card class="box-card">
          <div style="font-size: 25px;margin: 5px">未完成</div>
          <div v-for="(item,index) of itemArr" :key="item.id" style="overflow: hidden">
            <el-divider></el-divider>
            <p style="margin-left: 5px">{{index+1}} {{item.content}} {{item.datetime}}</p>
            <div class="btns">
              <el-button type="primary" @click="overItemList(index)">完成</el-button>
              <el-button type="primary" @click="removeItemList(index)">移除</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row class="items">
      <el-col :span="24">
        <el-card class="box-card">
          <div style="font-size: 25px;margin: 5px">已完成</div>
          <div v-for="(item,index) of overArr" :key="item.id" style="overflow: hidden">
            <el-divider></el-divider>
            <p class="overFont">{{index+1}} {{item.content}} {{item.datetime}}</p>
            <div class="btns">
              <el-button type="primary" @click="removeOverItemList(index)">移除</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "Home",
    data() {
      let itemArr = []
      let overArr = []
      this.$http.get('http://47.92.224.216:8001/api/findAll').then(function (res) {
        let data = res['body']['data']
        for (let i = 0; i < data['page']['incompleteCount']; i++) {
          itemArr.push(data['list']['incomplete'][i])
        }
        for (let i = 0; i < data['page']['completeCount']; i++) {
          overArr.push(data['list']['complete'][i])
        }
      }, function () {
        this.$message({
          message: '数据库读取失败',
          type: "warning"
        });
      })
      return {
        inputValue: '',
        itemArr: itemArr,
        overArr: overArr
      }
    },
    methods: {
      addItemList() {
        if (this.inputValue.trim().length === 0) {
          this.$message({
            message: '不能为空',
            type: "warning"
          });
          return;
        }
        let that=this
        this.$http.get('http://47.92.224.216:8001/api/add?content='+that.inputValue).then(function (res) {
          that.itemArr.push(res['body']['data'])
        }, function () {
          this.$message({
            message: '添加失败，服务器故障',
            type: "warning"
          });
        })

        this.inputValue = ""
      },
      removeItemList(index) {
        let that=this
        this.$http.get('http://47.92.224.216:8001/api/delete?id='+that.itemArr[index].id).then(function (res) {
          this.itemArr.splice(index, 1)
        }, function () {
          this.$message({
            message: '删除失败，服务器故障',
            type: "warning"
          });
        })
      },
      overItemList(index) {
        let that=this
        this.$http.get('http://47.92.224.216:8001/api/update?type=1&id='+that.itemArr[index].id).then(function (res) {
          let item = that.itemArr.splice(index, 1)
          that.overArr.push(item[0])
        }, function () {
          this.$message({
            message: '修改失败，服务器故障',
            type: "warning"
          });
        })
      },
      removeOverItemList(index) {
        let that=this
        this.$http.get('http://47.92.224.216:8001/api/delete?id='+that.overArr[index].id).then(function (res) {
          that.overArr.splice(index, 1)
        }, function () {
          this.$message({
            message: '删除失败，服务器故障',
            type: "warning"
          });
        })
      }

    }
  }
</script>

<style scoped>
  .width {
    width: 50%;
    margin: 0 auto;
  }

  @media only screen and (max-width: 1025px) {
    .width {
      width: 90%;
      margin: 0 auto;
    }
  }

  p {
    float: left;
  }

  .btns {
    float: right;
  }

  .items {
    margin-top: 30px;
  }

  .overFont {
    color: #ccc;
    margin-left: 5px;
  }
</style>
