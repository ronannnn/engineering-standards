# 多层模块格式与校验样例

这是虚构的回归夹具，演示两个两层模块 `users/access` 和 `orders/refund` 如何组织资料、隔离同名编号、汇总验收并统一交付。为验证命名空间，模块内容有意复用单目录优惠券样例，业务内容不是实际用户/订单设计，也不是已经执行的审批、部署或真实 Agent 试跑。

根目录保留系统级资料；模块各有 01–06 和 08，没有各自的 07。根 04 汇总模块任务与 AC；根 06 引用真实存在于模块报告中的限定用例；根 07 固定模块报告修订。公共基线记录根 01–03 的修订。

```bash
python3 gates/run.py examples/modular-run --all
python3 gates/run.py examples/modular-run --delivery
python3 gates/run.py examples/modular-run --module users --stage 06
```

修改模块测试或评审修订后，根 07 的快照也需复核更新；修改公共修订后，模块基线需按影响重新确认。不能只改数字让检查通过。
