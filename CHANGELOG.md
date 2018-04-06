# Changelog
工作记录小软件的更新日志，格式基于 [如何维护更新日志](https://keepachangelog.com/zh-CN/1.0.0/)。

## [Unreleased]
### Added
- 增加保密措施

## [0.5.2] - 2018-04-06
### Changed
- excel的sheetname和任务保持一致

## [0.5.1] - 2018-04-06
### Added
- 查询结果可以导出为Excel，并可选择是否立即打开
### Changed
- 查询结果窗口优化，现在会随着结果的数量变化
- 强迫症患者硬是把查询窗口和根窗口弄成一样宽了
- 日期选择说明改回“不选则默认当天”
### Fixed
- 现在必须选择分类才可以添加记录

## [0.4.2] - 2018-04-03
### Added
- 增加运行日志和错误日志
- 清空表和初始化要求确认
### Changed
- 数据库文件移到代码文件夹
### Fixed
- 现在没选择表就点击清空表，会弹出提示

## [0.3.3] - 2018-03-28
### Fixed
- QueryRoot类中忘记定义modified

## [0.3.2] - 2018-03-28
### Fixed
- 修改记录时若修改分类，原分类下记录未删除
- 修改记录后查询记录弹窗不能实时更新

## [0.3.1] - 2018-03-27
### Added
- 可以不选择分类就查询

## [0.2.1] - 2018-03-26
### Added
- 滚动条显示查询结果

### Changed
- 日期选择说明由“不选则默认当天”改为“当天添加记录可不选”

### Fixed
- 查询记录列表中点击灰色修改记录按钮会弹出修改弹窗

## 0.1.1 - 2018-03-21
- 初始版本

[Unreleased]: https://github.com/WolfWW/python-work-diary/compare/v0.5.2...HEAD
[0.5.2]: https://github.com/WolfWW/python-work-diary/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/WolfWW/python-work-diary/compare/v0.4.2...v0.5.1
[0.4.2]: https://github.com/WolfWW/python-work-diary/compare/v0.3.3...v0.4.2
[0.3.3]: https://github.com/WolfWW/python-work-diary/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/WolfWW/python-work-diary/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/WolfWW/python-work-diary/compare/v0.2.1...v0.3.1
[0.2.1]: https://github.com/WolfWW/python-work-diary/compare/v0.1.1...v0.2.1