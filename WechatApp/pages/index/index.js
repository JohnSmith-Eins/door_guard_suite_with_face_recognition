var util = require('../../utils/util.js');
var i=5;
Page({
  data: {
    time:"",
    time2:"",
    imgUr2: ""
  },
  fun() {
    var that = this;
    wx.request({
      url: 'https://gkmtz.hfzhang.wang/human/', 
      data: {
        x: '',
        y: ''
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success(res) {

        var time = util.formatTime(new Date())
        that.setData({
          time: time
        })
        let str = res.data
        console.log(str)
        var reg = /(?<=(href="))[^"]*?(?=")/ig;
        var allSrc = str.match(reg);
        console.log(allSrc)
        var aaa = allSrc[i].replace(/\"/g, "")
        console.log(aaa);
        that.setData({
          imgUr2: 'https://gkmtz.hfzhang.wang/human/' +aaa,
          time2: String(aaa)[0] + String(aaa)[1] + String(aaa)[2] + String(aaa)[3] +"/"+ String(aaa)[4] + String(aaa)[5] +"/"+ String(aaa)[6] + String(aaa)[7]+"/ " + String(aaa)[9] + String(aaa)[10]+":" + String(aaa)[11] + String(aaa)[12]+":" + String(aaa)[13] + String(aaa)[14] 
        })
        i=i+1;
      }
    })
  }
})
