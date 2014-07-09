from barrel import Store, Field, IntField
from barrel.rpc import RpcMixin


def document_converter(*args, **kwargs):
    from barrel_reaktor.document.models import Document
    return Document(*args, **kwargs)


class Category(Store, RpcMixin):
    interface = 'WSContentCategoryMgmt'

    id = Field(target='ID')
    name = Field(target='name')
    children_ids = Field(target='childrenIDs', default=[])
    count = IntField(target='count')
    document_ids = Field(target='documentIDs')
    filter = Field(target='filter')
    offset = IntField(target='offset')
    parent_id = Field(target='parentID', default=False)
    total_count = IntField(target='subtreeSize')

    @classmethod
    def get_by_id(cls, token, cat_id, with_children=True, offset='0', number_of_results=-1, sort=None, direction='asc'):
        invert = direction == 'desc'
        return cls.signature(method='getContentCategory',
                             args=[token, cat_id, with_children, sort, invert, offset, number_of_results])

    @classmethod
    def get_roots_by_token(cls, token, depth=0, min_number_of_documents=0):
        return cls.signature(method='getCatalogContentCategoryRootsForUser',
                             args=[token, depth, min_number_of_documents])

    @classmethod
    def get_documents(cls, token, cat_id, include_sub_cats=False, offset=0, number_of_results=-1, sort=None, direction='asc'):
        invert = direction == 'desc'
        return cls.signature(interface='WSDocMgmt', method='getDocumentsInContentCategory',
                             args=[token, cat_id, include_sub_cats, sort, invert, offset, number_of_results],
                             data_converter=document_converter)
