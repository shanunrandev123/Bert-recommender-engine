import torch
import torch.nn as nn
import numpy as np

def loss_fn(outputs, targets):
	return nn.BCEWithLogitsLoss()(outputs, targets.view(-1,1))


def train_fn(data_loader, model, optimizer, device, scheduler):
	model.train()

	for d in data_loader:
		ids = d["ids"]
		token_type_ids = d["token_type_ids"]
		mask = d["mask"]
		targets = d["targets"]

		ids = ids.to(device, dtype=torch.long)
		token_type_ids = token_type_ids.to(device, dtype=torch.long)

		mask = mask.to(device, dtype = torch.long)
		targets = targets.to(device, dtype = torch.float)

		optimizer.zero_grad()
		outputs = model(ids=ids, mask=mask, token_type_ids=token_type_ids)

		loss = loss_fn(outputs, targets)
		loss.backward()
		optimizer.step()
		scheduler.step()


def eval_fn(data_loader, model, device):
	model.eval()
	fin_targets = []
	fin_outputs = []
	with torch.no_grad():
		for d in data_loader:
			ids = d["ids"]
			token_type_ids = d["token_type_ids"]
			mask = d["mask"]
			targets = d["targets"]
			ids = ids.to(device, dtype=torch.long)
			token_type_ids = token_type_ids.to(device, dtype=torch.long)
			mask = mask.to(device, dtype=torch.long)
			targets = targets.to(device, dtype=torch.float)
			outputs = model(ids=ids, mask=mask, token_type_ids=token_type_ids)

			targets = targets.cpu().detach()
			fin_targets.extend(targets.np().tolist())
			outputs = torch.sigmoid(outputs).cpu().detach()
			fin_outputs.extend(outputs.np().tolist())

	return fin_outputs, fin_targets







