#include "src/ExpRunner.h"
#include <iostream>
#include <memory>
#include <torch/torch.h>

int main(int argc, char *argv[]) {
  std::cout << "Aoligei!" << std::endl;
  torch::manual_seed(2022);
  std::string conf_path = argv[1];
  auto exp_runner = std::make_unique<ExpRunner>(conf_path);
  exp_runner->Execute();
  return 0;
}
