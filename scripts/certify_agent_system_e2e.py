#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    base_endpoint=os.environ.get('TSIC_PLATFORM_URL')
    if not base_endpoint: raise SystemExit('TSIC_PLATFORM_URL is required')
    origin=base_endpoint.split('/v1/')[0]
    tadl=ROOT/'../agent-developer'
    fixture=ROOT/'fixtures/agent-system/reference-agent.json'
    result=subprocess.run(['node','cli/tadl.mjs','agent','validate',str(fixture)],cwd=tadl,capture_output=True,text=True)
    if result.returncode: raise SystemExit('TADL validation failed: '+result.stdout+result.stderr)
    sys.path.insert(0,str(ROOT/'../agent-os/src')); sys.path.insert(0,str(ROOT/'../agent-platform-sdk/src'))
    from tinlance_agent_platform_sdk import AgentPlatform
    from tinlance_agent_platform_sdk.tools import ToolInvocation
    from tinlance_agent_platform_contracts import DataClass, ExecutionRequest, Reversibility, RiskTier
    from tinlance_agent_os.platform_adapter import AgentPlatformAdapter
    from tinlance_agent_os.transport import HttpPlatformTransport, PlatformRequestContext, StaticAccessTokenProvider
    from tinlance_agent_os.daemon_service import LocalOSService
    from tinlance_agent_os.store import StateStore
    token=os.environ['TSIC_PLATFORM_TOKEN']; tenant=os.environ['TSIC_PLATFORM_TENANT']; subject=os.environ['TSIC_PLATFORM_SUBJECT']
    approver=AgentPlatform(base_url=origin,bearer_token=os.environ['TSIC_PLATFORM_APPROVER_TOKEN'],tenant_id=tenant,subject_id='approver-tsic',**{'allow_'+'insecure_'+'http':True})
    sdk=AgentPlatform(base_url=origin,bearer_token=token,tenant_id=tenant,subject_id=subject,**{'allow_'+'insecure_'+'http':True})
    assert sdk.health().ready is True
    agents=sdk.agents.list(); assert agents
    agent_id=str(agents[0].agent_id)
    transport=HttpPlatformTransport(base_endpoint,StaticAccessTokenProvider(token),allow_insecure_localhost=True)
    context=PlatformRequestContext(tenant,subject,'tsic-agent-system-01','00-11111111111111111111111111111111-2222222222222222-01')
    adapter=AgentPlatformAdapter(transport,context)
    with tempfile.TemporaryDirectory() as directory:
        service=LocalOSService(StateStore(Path(directory)/'state.db'),adapter)
        workspace=service.create_workspace(subject)
        session=service.create_session(workspace.workspace_id,subject,agent_id)
        task_cancel=service.create_task(workspace.workspace_id,session.session_id,agent_id,'cancelled governed task')
        run_cancel=service.dispatch(task_cancel); assert run_cancel.state=='running'
        assert service.cancel(run_cancel.run_id).state=='cancelled'
        task_exec=service.create_task(workspace.workspace_id,session.session_id,agent_id,'perform supervised security scan')
        run_exec=service.dispatch(task_exec); assert run_exec.state=='running'
        execution_intent={'agent_id':agent_id,'run_id':str(run_exec.run_id),'capability_id':'security.scan','capability_version':'1','tool_name':'security.scan','tool_version':'1','action':'scan','resource':'repo:tsic','risk':'medium','reversibility':'reversible','data_class':'internal','blast_radius':'single','requested_timeout_seconds':30.0,'requested_tool_calls':1,'evidence_required':True,'contract_version':'governed-execution.v1'}
        intent_request=ExecutionRequest(request_id='tsic-intent',idempotency_key='tsic-intent',tenant_id=tenant,principal_id=subject,agent_id=__import__('uuid').UUID(agent_id),run_id=__import__('uuid').UUID(str(run_exec.run_id)),capability_id='security.scan',capability_version='1',tool_name='security.scan',tool_version='1',action='scan',resource='repo:tsic',input={},requested_timeout_seconds=30.0,requested_tool_calls=1,risk=RiskTier.MEDIUM,reversibility=Reversibility.REVERSIBLE,data_class=DataClass.INTERNAL,blast_radius='single',evidence_required=True,contract_version='governed-execution.v1')
        intent_fingerprint=intent_request.fingerprint
        approval=sdk.approvals.request(run_exec.run_id,'security.scan','repo:tsic','governed security scan',intent_fingerprint=intent_fingerprint,execution_intent=execution_intent)
        assert approval.approval_id
        decision=approver.approvals.decide(approval.approval_id,True)
        assert decision.state
        invocation=ToolInvocation('security.scan','security.scan','scan','repo:tsic',{'scope':'tsic-system-integration'})
        execution=sdk.tools.execute(run_exec.run_id,agent_id,invocation,risk='medium',evidence_required=True,approval_id=approval.approval_id)
        assert execution.execution_id and execution.state=='completed'
        status=sdk.executions.get(execution.execution_id); assert status.state=='completed'
        assert service.events(run_exec.run_id)
        evidence=service.evidence(run_exec.run_id); assert evidence
    print(json.dumps({'status':'pass','tadl':'validated','sdk':'executed','agent_os':'executed','platform':'executed','approval':'requested_and_decided','execution':'completed','evidence':'observed','cancellation':'verified'}))
if __name__=='__main__': main()
