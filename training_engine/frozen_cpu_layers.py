"""Keep frozen IO matrices on CPU, with optional CPU-resident output logits."""
def offload_frozen_io(model,keep_output_on_cpu=False):
    import types,os,json
    import torch
    modules=[];output=model.get_output_embeddings()
    for module in (model.get_input_embeddings(),output):
        if any(module is existing for existing in modules):continue
        modules.append(module);module.to('cpu');original=module.forward
        head=module is output
        def forward(self,value,*args,_original=original,_head=head,**kwargs):
            destination=value.device;trace=os.environ.get('NOTELLA_TRAIN_TRACE')=='1' and _head
            if trace:print(json.dumps(dict(completionStage='frozen_output_forward',inputShape=list(value.shape),weightDtype=str(self.weight.dtype))),flush=True)
            result=_original(value.to('cpu'),*args,**kwargs)
            if trace:print(json.dumps(dict(completionStage='frozen_output_done',outputShape=list(result.shape))),flush=True)
            return result if _head and keep_output_on_cpu else result.to(destination)
        module.forward=types.MethodType(forward,module)
    if torch.cuda.is_available():torch.cuda.empty_cache()
    return modules
