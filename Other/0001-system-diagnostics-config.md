# system.diagnostics 相关配置

## EF 取消 SQL 输出

``` XML
<!--调试时候，EF 取消 sql 输出到 output 窗口-->
<system.diagnostics>
<sources>
    <source name="FirebirdSql.Data.FirebirdClient">
    <listeners>
        <clear />
    </listeners>
    </source>
</sources>
</system.diagnostics>

使用EF 表必须包含主键
```

## WCF 调试代码输出，用于序列号

``` XML
<system.diagnostics>
    <sources>
      <source name="System.ServiceModel.MessageLogging" switchValue="Warning, ActivityTracing">
        <listeners>
          <add name="ServiceModelTraceListener" />
        </listeners>
      </source>
      <source name="System.ServiceModel" switchValue="Verbose,ActivityTracing">
        <listeners>
          <add name="ServiceModelTraceListener" />
        </listeners>
      </source>
      <source name="System.Runtime.Serialization" switchValue="Verbose,ActivityTracing">
        <listeners>
          <add name="ServiceModelTraceListener" />
        </listeners>
      </source>
    </sources>
    <sharedListeners>
      <add initializeData="App_tracelog.svclog" type="System.Diagnostics.XmlWriterTraceListener, System, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089" name="ServiceModelTraceListener" traceOutputOptions="Timestamp" />
    </sharedListeners>
  </system.diagnostics>
```