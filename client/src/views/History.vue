<template>
    <el-main>
        <p class="empty-content" v-if="visible1">{{ emptyMessage }}</p>
        <div>
            <el-row class="el-row1">
                <el-col :span="24">
                    <span class="demonstration">{{$t('historyPage.range')}}</span>
                    <el-date-picker
                        v-model="timeValue"
                        type="daterange"
                        unlink-panels
                        :range-separator="$t('historyPage.to')"
                        :start-placeholder="$t('historyPage.StartDate')"
                        :end-placeholder="$t('historyPage.endDate')"
                        :picker-options="pickerOptions"
                        value-format="yyyy-MM-dd"
                        @change="onSubmit">
                    </el-date-picker>
                </el-col>
            </el-row>
            <el-row class="el-row2" v-if="visible2">
				       <div class="pic1">
                    <div id="scoreLine" style="width:100%; height:300px">
                        <!-- 此处为总得分统计折线图 -->
                    </div>
                </div>
					<div class="mistake_word">
					     <el-col :span="24">
                    <!-- TODO: 错字表 -->
                    <el-card class="mistake-card">
                        <el-table
                            :data="tableData"
                            style="width: 100"
							height="270"
                            :default-sort = "{prop: 'num', order: 'descending'}"
                            >
                            <el-table-column
                                prop="wrongchar"
                                :label="$t('historyPage.typos')"
								align="center"
                                width="195">
                            </el-table-column>
                            <el-table-column
                                prop="num"
                                :label="$t('historyPage.wrongtimes')"
								align="center"
                                width="180">
                            </el-table-column>
                        </el-table>
                    </el-card>
                </el-col>
				</div>
            </el-row>
            <el-row class="el-row2" v-if="visible2">
              <div class="pic2">
						<div id="vocabularyLine" style="width:100%; height:300px">
							<!-- 此处为词汇水平得分统计折线图 -->
			  </div>
          </div>
              <div class="pic3">
						<div id="wrongcharChart" style="width:100%; height:300px">
						<!-- 此处为错别字统计柱状图 -->
              </div>
          </div>
            </el-row>
        </div>
    </el-main>
</template>

<script>
    import https from '../api/https.js'
    import echarts from 'echarts'

    export default {
        data () {
            return {
                emptyMessage: '',
                visible1: false,
                visible2: true,
                visible3: true,
                records: [],
                wrongchars: {},
                suggestion: '',
                vocabulary: 0,
                vocabularySuggestion: '',
                tableData: [],
                pickerOptions: {
                    shortcuts: [
                        {
                            text: this.$t('historyPage.pickerOptions1'),
                            onClick (picker) {
                                const end = new Date();
                                const start = new Date();
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                                picker.$emit('pick', [start, end]);
                            }
                        },
                        {
                            text: this.$t('historyPage.pickerOptions2'),
                            onClick (picker) {
                                const end = new Date();
                                const start = new Date();
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                                picker.$emit('pick', [start, end]);
                            }
                        },
                        {
                            text: this.$t('historyPage.pickerOptions3'),
                            onClick (picker) {
                                const end = new Date();
                                const start = new Date();
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                                picker.$emit('pick', [start, end]);
                            }
                        }
                    ]
                },
                timeValue: ''
            }
        },
        // 初始化页面显示全部记录的数据
        mounted () {
            https.fetchGet('history').then((res) => {
                if (res.data['code'] === 200) {
                    if (res.data['records']) {
                        this.records = res.data['records'];
                        this.wrongchars = res.data['wrongchars'];
                        this.initDataTable();
                        this.suggestion = res.data['suggestion'];
                        this.vocabulary = res.data['vocabulary'];
                        this.vocabularySuggestion = res.data['vocabularySuggestion'];

                        if (JSON.stringify(this.wrongchars) === '{}') {
                            this.visible3 = false;
                        } else {
                            this.drawWrongcharChart();
                        }

                        this.drawScoreLine();
                        this.drawVocabularyLine();
                    } else {
                        this.visible1 = true;
                        this.visible2 = false;
                        this.emptyMessage = res.data['message'];
                    }
                    return true;
                } else {
                    return false;
                }
            });
        },
        methods: {
            onSubmit () {
                var startTime = this.timeValue[0];
                var endTime = this.timeValue[1];
                var timeInfo = {'startTime': startTime, 'endTime': endTime};

                this.visible1 = false;
                this.visible2 = true;

                https.fetchPost('history', timeInfo).then((res) => {
                    if (res.data['code'] === 200) {
                        if (res.data['records']) {
                            this.records = res.data['records'];
                            this.wrongchars = res.data['wrongchars'];
                            this.initDataTable();
                            this.suggestion = res.data['suggestion'];
                            this.vocabulary = res.data['vocabulary'];
                            this.vocabularySuggestion = res.data['vocabularySuggestion'];

                            if (JSON.stringify(this.wrongchars) === '{}') {
                                this.visible3 = false;
                            } else {
                                this.drawWrongcharChart();
                            }

                            this.drawScoreLine();
                            this.drawVocabularyLine();
                        } else {
                            this.visible1 = true;
                            this.visible2 = false;
                            this.emptyMessage = res.data['message'];
                        }
                        return true;
                    } else {
                        return false;
                    }
                });
            },
            initDataTable () {
                for (var key in this.wrongchars) {
                    this.tableData.push({wrongchar: key, num: this.wrongchars[key]});
                }
            },
            drawScoreLine () {
                var myChart = echarts.init(document.getElementById('scoreLine'));
                var option = {
                    title: {
                        text: '总得分统计图',
                        color:'#337afb',
                    },
                    xAxis: {
						name:'次数',
						nameTextStyle:{
							fontSize:10
						},
                        type: 'category',
                        data: []
                    },
                    yAxis: {
						name:'分值',
						nameTextStyle:{
							fontSize:10
						},
                        type: 'value',
                        max: 100
                    },
                    series: [{
                        data: [],
                        type: 'line'
                    }]
                };
                var x = []
                var y = []
                var n = 1;
                for (let index in this.records) {
                    x.push(n);
                    n = n + 1;
                    y.push(this.records[index].totalScore);
                }
                option.xAxis.data = x;
                option.series[0].data = y;
                myChart.setOption(option);
            },
            drawVocabularyLine () {
                var myChart = echarts.init(document.getElementById('vocabularyLine'));

                var option = {
                    title: {
                        text: '词汇水平得分统计图'
                    },
                    xAxis: {
						name:'次数',
						nameTextStyle:{
							fontSize:10
						},
                        type: 'category',
                        data: []
                    },
                    yAxis: {
						name:'等级',
						nameTextStyle:{
							fontSize:10
						},
                        type: 'value',
                        max: 5
                    },
                    series: [{
                        data: [],
                        type: 'line'
                    }]
                };
                var x = []
                var y = []
                var n = 1;
                for (let index in this.records) {
                    x.push(n);
                    n = n + 1;
                    y.push(this.records[index].vocabularyLevel);
                }
                option.xAxis.data = x;
                option.series[0].data = y;
                myChart.setOption(option);
            },
            drawWrongcharChart () {
                var myChart = echarts.init(document.getElementById('wrongcharChart'));

                var dataAxis = [];
                var data = [];
                for (let key in this.wrongchars) {
                    dataAxis.push(key);
                    data.push(this.wrongchars[key]);
                }
                var yMax = 20;
                var dataShadow = [];

                for (var i = 0; i < data.length; i++) {
                    dataShadow.push(yMax);
                }

                var option = {
                    title: {
                        text: '错别字统计图'
                    },
                    xAxis: {
                        data: dataAxis,
                        axisLabel: {
                            inside: true,
                            textStyle: {
                                color: '#fff'
                            }
                        },
                        axisTick: {
                            show: false
                        },
                        axisLine: {
                            show: false
                        },
                        z: 10
                    },
                    yAxis: {
                        axisLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        },
                        axisLabel: {
                            textStyle: {
                                color: '#999'
                            }
                        }
                    },
                    dataZoom: [
                        {
                            type: 'inside'
                        }
                    ],
                    series: [
                        { // For shadow
                            type: 'bar',
                            itemStyle: {
                                color: 'rgba(0,0,0,0.05)'
                            },
                            barGap: '-100%',
                            barCategoryGap: '40%',
                            data: dataShadow,
                            animation: false
                        },
                        {
                            type: 'bar',
                            itemStyle: {
                                color: new echarts.graphic.LinearGradient(
                                    0, 0, 0, 1,
                                    [
                                        {offset: 0, color: '#83bff6'},
                                        {offset: 0.5, color: '#188df0'},
                                        {offset: 1, color: '#188df0'}
                                    ]
                                )
                            },
                            emphasis: {
                                itemStyle: {
                                    color: new echarts.graphic.LinearGradient(
                                        0, 0, 0, 1,
                                        [
                                            {offset: 0, color: '#2378f7'},
                                            {offset: 0.7, color: '#2378f7'},
                                            {offset: 1, color: '#83bff6'}
                                        ]
                                    )
                                }
                            },
                            data: data
                        }
                    ]
                };

                // Enable data zoom when user click bar.
                var zoomSize = 6;
                myChart.on('click', function (params) {
                    console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
                    myChart.dispatchAction({
                        type: 'dataZoom',
                        startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
                        endValue: dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
                    });
                });

                myChart.setOption(option);
            }
        }
    }
</script>

<style lang="scss" scoped>
    .mistake-card {
        //background-color: aquamarine;
        background-color: ghostwhite;
        text-align: left;
        height: 300px;
        //padding-top:5px;
        border-radius: 10px;
        -moz-box-shadow:2px 2px 5px #333333;
        -webkit-box-shadow:2px 2px 5px #333333;
        box-shadow: 7px 15px 30px #285a63;
    }
    .sugg1{
          color: #ff724c;
          font-weight: bold;
          font-size:21px;
          background-color: rgba(253, 232, 213, 0.98);
	      	border-radius: 10px;
		      /*阴影*/
		      -moz-box-shadow:1px 1px 1px #59bbbb;             -webkit-box-shadow:1px 1px 1px #bcfcff;
	      	box-shadow: 5px 10px 10px #fde8d5;
    }

    .sugg2{
          color: #ff724c;
          font-weight: bold;
          font-size:21px;
          background-color: rgba(253, 232, 213, 0.98);
	      	border-radius: 10px;
		      /*阴影*/
		      -moz-box-shadow:1px 1px 1px #59bbbb;             -webkit-box-shadow:1px 1px 1px #bcfcff;
	      	box-shadow: 5px 10px 10px #fde8d5;
    }
    .number{
      font-size:20px;
      font-weight:bold;
      color:#ff724c;
    }
    .el-row1 {
        margin:15px 80px 20px 20px;
    }
    .el-row2 {
        margin-top: 60px;
    }
    p {
        margin-top: -10px;
    }
	.pic1{
		background-color: ghostwhite;
		position:relative;
		margin-left:40px;
		width:420px;
		border-radius: 10px;
		-moz-box-shadow:2px 2px 5px #333333;
		-webkit-box-shadow:2px 2px 5px #333333;
		box-shadow: 7px 15px 30px #285a63;
	}
	.mistake_word{
		background-color: ghostwhite;
		position:absolute;
		margin-left:505px;
		margin-top:-302px;
		width:420px;
		border-radius: 10px;
		-moz-box-shadow:2px 2px 5px #333333;
		-webkit-box-shadow:2px 2px 5px #333333;
		box-shadow: 7px 15px 30px #285a63;
	}
    .pic2{
		background-color: ghostwhite;
		position:relative;
		margin-left:40px;
		margin-bottom:20px;
		width:420px;
		border-radius: 10px;
		-moz-box-shadow:2px 2px 5px #333333;
		-webkit-box-shadow:2px 2px 5px #333333;
		box-shadow: 7px 15px 30px #285a63;
	}
	.pic3{
		background-color: ghostwhite;
		position:absolute;
		margin-left:505px;
		margin-top:-322px;
		margin-bottom:20px;
		width:420px;
		border-radius: 10px;
		-moz-box-shadow:2px 2px 5px #333333;
		-webkit-box-shadow:2px 2px 5px #333333;
		box-shadow: 7px 15px 30px #285a63;
	}
</style>
