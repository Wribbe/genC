DIR_GEN := gen
DIR_SCR := src
DIR_BIN := bin

DIRS := $(DIR_GEN) $(DIR_SRC) $(DIR_BIN)

C_FILES := $(patsubst %.py,$(DIR_GEN)/%.c,$(notdir $(wildcard $(DIR_SCR)/*.py)))
BINS :=  $(patsubst %.c,$(DIR_BIN)/%,$(notdir $(C_FILES)))

all: $(C_FILES) $(BINS) | $(DIRS)

$(DIR_GEN)/%.c : $(DIR_SCR)/%.py
	./$^ > $@

$(DIR_BIN)/% : $(DIR_GEN)/%.c
	gcc $^ -o $@

$(DIRS):
	@mkdir $@
