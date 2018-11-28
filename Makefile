DIR_GEN := gen
DIR_SRC := src
DIR_BIN := bin
DIR_DBS := dbs
DIR_SRC_SQL := $(DIR_SRC)/sql

DIRS := $(DIR_GEN) $(DIR_SRC) $(DIR_BIN) $(DIR_DBS)

C_FILES := $(patsubst %.py,$(DIR_GEN)/%.c,$(notdir $(wildcard $(DIR_SRC)/*.py)))
BINS :=  $(patsubst %.c,$(DIR_BIN)/%,$(notdir $(C_FILES)))
SQL_SCHEMAS := $(wildcard $(DIR_SRC_SQL)/*.sql)
DBS := $(patsubst %.sql,$(DIR_DBS)/%.sqlite3,$(notdir $(SQL_SCHEMAS)))

all: $(C_FILES) $(BINS) $(DBS)

$(DIR_GEN)/%.c : $(DIR_SRC)/%.py | $(DIR_GEN)
	./$^ > $@

$(DIR_BIN)/% : $(DIR_GEN)/%.c | $(DIR_BIN)
	gcc $^ -o $@

$(DIR_DBS)/%.sqlite3 : $(DIR_SRC_SQL)/%.sql | $(DIR_DBS)
	./db.py init $^ -o $@

$(DIRS):
	@mkdir $@
