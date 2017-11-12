// 测量某个 element 的宽、高、x、y
// 方法一：
var height = await page.evaluate(function() {
	const rect = document.querySelector('#J-list-box').getBoundingClientRect();
	// rect = {left: 10, top: 10, width: 10, height: 10}
	return rect.height;
})
// 方法二：
const elementHandle = await page.$('#J-list-box');
const box = await elementHandle.boundingBox();
// box = { x: 100, y: 50, width: 50, height: 50 }

// 遍历某类 element 并执行一遍相同的操作
// example：点击当前页面所有 .more-icon 元素
const moreIconList = await page.$$('.more-icon');
await Promise.all(moreIconList.map(icon => {
	page.evaluate(i => i.click(), icon)
}));