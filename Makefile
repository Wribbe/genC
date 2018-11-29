DIR_GEN := gen
DIR_SRC := src
DIR_BIN := bin
DIR_DBS := dbs
DIR_SRC_SQL := $(DIR_SRC)/sql
DIR_BIN_UTILS := $(DIR_BIN)/utils

PERCENT := %
$(eval DIRS := $(foreach var,$(filter-out %_$(PERCENT)%,$(filter DIR_%,$(shell cat Makefile))),$$($(var))))

C_FILES := $(patsubst %.py2c,$(DIR_GEN)/%.c,$(notdir $(wildcard $(DIR_SRC)/*.py2c)))
SQL_SCHEMAS := $(wildcard $(DIR_SRC_SQL)/*.sql)

BINS := $(patsubst %.c,$(DIR_BIN)/%,$(notdir $(C_FILES)))
BINS_UTILS := $(patsubst %.py,$(DIR_BIN_UTILS)/%,$(notdir $(wildcard $(DIR_SRC)/*.py)))

DBS := $(patsubst %.sql,$(DIR_DBS)/%.sqlite3,$(notdir $(SQL_SCHEMAS)))
PIPELINES := $(patsubst %.pipes,$(DIR_BIN)/%.pipeline,$(notdir $(wildcard $(DIR_SRC)/*.pipes)))

all: $(C_FILES) $(BINS_UTILS) $(BINS) $(DBS) $(PIPELINES)

$(DIR_GEN)/%.c : $(DIR_SRC)/%.py2c | $(DIR_GEN)
	./$^ > $@

$(DIR_BIN)/% : $(DIR_GEN)/%.c | $(DIR_BIN)
	gcc $^ -o $@

$(DIR_BIN_UTILS)/% : $(DIR_SRC)/%.py | $(DIR_BIN_UTILS)
	cp $^ $@
	chmod +x $@

$(DIR_DBS)/%.sqlite3 : $(DIR_SRC_SQL)/%.sql | $(DIR_DBS)
	./db.py init $^ -o $@

$(DIR_BIN)/%.pipeline : $(DIR_SRC)/%.pipes $(DIR_BIN_UTILS)/construct_pipeline
	$(filter $(DIR_BIN)%,$^) $(filter %.pipes,$^) -o $@
	chmod +x $@

$(DIRS):
	@mkdir -p $@
