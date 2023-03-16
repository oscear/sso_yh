const page={
  index:"/bi/Viewer?proc=0&action=index",
  conn:"/bi/Viewer?proc=0&action=conn",
  query:"/bi/Viewer?proc=0&action=query",
  editor:"/bi/Viewer?showOthers=true&proc=0&action=editor",
  viewerManager:"/bi/Viewer?proc=0&action=viewerManager",
  schedule:"/bi/Viewer?proc=9&req=800&resource=schedule",
  ml:"/bi/Viewer?proc=0&action=ml",
  portal:"/bi/Viewer?proc=0&action=portal",
  workflow:"/bi/Viewer?proc=0&action=businessProcess#/biworkflow-manage",
  system:"/bi/Viewer?proc=0&action=system",
  sysMgr:"/bi/Viewer?proc=0&action=system&_trace_=sysMgr",
  secure:"/bi/Viewer?proc=0&action=system&_trace_=secure",
  logMgr:"/bi/Viewer?proc=0&action=system&_trace_=logMgr",
  audit:"/bi/Viewer?proc=0&action=system&_trace_=audit",
  deploy:"/bi/Viewer?proc=0&action=system&_trace_=deploy",
  VooltDBMgr:"/bi/Viewer?proc=0&action=system&_trace_=VooltDBMgr",
  DBMgr:"/bi/Viewer?proc=0&action=system&_trace_=DBMgr",
  enterpriseMgr:"/bi/Viewer?proc=0&action=system&_trace_=enterpriseMgr",
  check:"/bi/Viewer?proc=0&action=system&_trace_=check",
  pluginMgr:"/bi/Viewer?proc=0&action=system&_trace_=pluginMgr",
}

const allpage=[
  {label:"index",alias:"首页",alias:"首页",url:"/bi/Viewer?proc=0&action=index"},
  {label:"conn",alias:"数据源",url:"/bi/Viewer?proc=0&action=conn"},
  {label:"query",alias:"数据集",url:"/bi/Viewer?proc=0&action=query"},
  {label:"editor",alias:"制作报告",url:"/bi/Viewer?proc=0&action=editor"},
  {label:"viewerManager",alias:"查看报告",url:"/bi/Viewer?proc=0&action=viewerManager"},
  {label:"schedule",alias:"调度任务",url:"/bi/Viewer?proc=9&req=800&resource=schedule"},
  {label:"ml",alias:"深度分析",url:"/bi/Viewer?proc=0&action=ml"},
  {label:"portal",alias:"制作门户",url:"/bi/Viewer?proc=0&action=portal"},
  {label:"workflow",alias:"流程审批",url:"/bi/Viewer?proc=0&action=businessProcess#/biworkflow-manage"},
  {label:"system",alias:"管理系统",url:"/bi/Viewer?proc=0&action=system"},
  {label:"sysMgr",alias:"管理系统-系统设置页面",url:"/bi/Viewer?proc=0&action=system&_trace_=sysMgr"},
  {label:"secure",alias:"管理系统-认证授权页面",url:"/bi/Viewer?proc=0&action=system&_trace_=secure"},
  {label:"logMgr",alias:"管理系统-日志管理页面",url:"/bi/Viewer?proc=0&action=system&_trace_=logMgr"},
  {label:"audit",alias:"管理系统-监控预警页面",url:"/bi/Viewer?proc=0&action=system&_trace_=audit"},
  {label:"deploy",alias:"管理系统-资源部署页面",url:"/bi/Viewer?proc=0&action=system&_trace_=deploy"},
  {label:"VooltDBMgr",alias:"管理系统-VooltDB管理",url:"/bi/Viewer?proc=0&action=system&_trace_=VooltDBMgr"},
  {label:"DBMgr",alias:"管理系统-数据库管理页面",url:"/bi/Viewer?proc=0&action=system&_trace_=DBMgr"},
  {label:"enterpriseMgr",alias:"管理系统-企业应用配置页面",url:"/bi/Viewer?proc=0&action=system&_trace_=enterpriseMgr"},
  {label:"check",alias:"管理系统-系统检查页面",url:"/bi/Viewer?proc=0&action=system&_trace_=check"},
  {label:"pluginMgr",alias:"管理系统-应用管理页面",url:"/bi/Viewer?proc=0&action=system&_trace_=pluginMgr"}
]

export default {page,allpage}