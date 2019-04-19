var chart = Highcharts.chart('container', {
	data: {
		table: 'datatable'
	},
	chart: {
		type: 'column'
	},
	title: {
		text: 'Number of Publications'
		// 该功能依赖 data.js 模块，详见https://www.hcharts.cn/docs/data-modules
	},
	yAxis: {
		allowDecimals: false,
		title: {
			text: '',
			rotation: 0
		}
	},
	tooltip: {
		formatter: function () {
			return this.point.y;
		}
	}
});